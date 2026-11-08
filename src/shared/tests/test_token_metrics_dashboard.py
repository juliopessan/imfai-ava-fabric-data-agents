"""
Tests for the Token Metrics Dashboard — rendering, cost and viewports (1440 px / 390 px).
"""

import pytest

from src.shared.scripts.execution_telemetry import ExecutionTelemetry
from src.shared.scripts.headroom_context_manager import CompressionStats
from src.shared.scripts.token_metrics_dashboard import (
    CompressionMetrics,
    ModelPrice,
    RunMetrics,
    calculate_cost,
    compression_from_stats,
    render_dashboard,
    run_from_telemetry_report,
)

VIEWPORTS = [("desktop", 1440, 900), ("mobile", 390, 844)]

PRICES = {
    "model-a": ModelPrice(input_price=3.0, output_price=15.0, unit="per_1m_tokens"),
    "model-k": ModelPrice(input_price=0.002, output_price=0.006, unit="per_1k_tokens"),
}

FULL_RUN = RunMetrics(
    run_id="run-full",
    model="model-a",
    input_tokens=130_808,
    output_tokens=65_404,
    compression=CompressionMetrics(
        input_tokens=130_808, output_tokens=39_242, compression_ratio=0.70, method="headroom"
    ),
)
EMPTY_RUN = RunMetrics(run_id="run-empty")
FULL_RUN_COST = 130_808 / 1_000_000 * 3.0 + 65_404 / 1_000_000 * 15.0


def _text(page, testid):
    return page.locator(f'[data-testid="{testid}"]').first.inner_text().strip()


class TestRenderValues:
    def test_displayed_values_match_input(self):
        html = render_dashboard([FULL_RUN], PRICES)
        assert 'data-testid="input-tokens">130,808<' in html
        assert 'data-testid="output-tokens">65,404<' in html
        assert 'data-testid="compression-ratio">70.0%<' in html
        assert 'data-testid="compression-method">headroom<' in html
        assert 'data-testid="tokens-saved">91,566<' in html
        assert 'data-testid="empty-state"' not in html

    def test_empty_run_shows_empty_state_without_savings(self):
        html = render_dashboard([EMPTY_RUN], PRICES)
        assert 'data-testid="empty-state"' in html
        assert "Sem métricas observadas" in html
        assert "savings-usd" not in html
        assert "tokens-saved" not in html
        assert "Economia" not in html

    def test_no_runs_shows_empty_state(self):
        html = render_dashboard([], PRICES)
        assert 'data-testid="empty-state"' in html
        assert "savings-usd" not in html

    def test_missing_metric_is_unavailable(self):
        run = RunMetrics(run_id="partial", input_tokens=10, output_tokens=5)
        html = render_dashboard([run], PRICES)
        assert 'data-testid="compression-ratio">Indisponível<' in html
        assert 'data-testid="cost-usd">Indisponível<' in html
        assert "savings-usd" not in html

    def test_mock_compression_is_flagged(self):
        run = RunMetrics(
            run_id="mock",
            compression=CompressionMetrics(100, 50, 0.5, method="mock"),
        )
        assert "mock-note" in render_dashboard([run], PRICES)

    def test_run_id_is_escaped(self):
        html = render_dashboard([RunMetrics(run_id="<script>x</script>")], PRICES)
        assert "<script>x</script>" not in html


class TestCost:
    def test_cost_per_million_tokens(self):
        cost = calculate_cost("model-a", 130_808, 65_404, PRICES)
        assert cost.amount_usd == pytest.approx(FULL_RUN_COST)
        assert cost.unit == "per_1m_tokens"

    def test_cost_per_thousand_tokens(self):
        cost = calculate_cost("model-k", 2_000, 1_000, PRICES)
        assert cost.amount_usd == pytest.approx(2 * 0.002 + 1 * 0.006)
        assert cost.unit == "per_1k_tokens"

    def test_rendered_cost_and_unit(self):
        html = render_dashboard([FULL_RUN], PRICES)
        assert f'data-testid="cost-usd">{FULL_RUN_COST:.6f}<' in html
        assert 'data-testid="price-unit">USD / 1M tokens<' in html

    def test_unknown_model_has_no_cost(self):
        assert calculate_cost("other", 1, 1, PRICES) is None
        assert calculate_cost(None, 1, 1, PRICES) is None

    def test_invalid_unit_rejected(self):
        with pytest.raises(ValueError):
            ModelPrice(1.0, 1.0, unit="per_banana")


class TestExistingInterfaces:
    def test_from_compression_stats(self):
        stats = CompressionStats(
            source_agent="a",
            target_agent="b",
            input_tokens=1000,
            output_tokens=400,
            compression_ratio=0.6,
            tokens_saved=600,
            latency_ms=1.0,
            method="mock",
            timestamp="2026-01-01T00:00:00",
        )
        comp = compression_from_stats(stats)
        assert (comp.input_tokens, comp.output_tokens, comp.method) == (1000, 400, "mock")
        assert comp.tokens_saved == 600
        assert compression_from_stats(stats.to_dict()) == comp

    def test_from_execution_telemetry(self):
        telemetry = ExecutionTelemetry("wf", "agent")
        telemetry.input_tokens = 1200
        telemetry.output_tokens = 300
        run = run_from_telemetry_report("r1", telemetry.generate_report())
        assert (run.input_tokens, run.output_tokens) == (1200, 300)
        assert run.compression is None


@pytest.fixture(scope="module")
def browser():
    sync_api = pytest.importorskip("playwright.sync_api", reason="playwright not installed")
    with sync_api.sync_playwright() as pw:
        try:
            instance = pw.chromium.launch()
        except Exception as exc:  # browser binary missing
            pytest.skip(f"chromium not available (run: playwright install chromium): {exc}")
        yield instance
        instance.close()


@pytest.mark.parametrize("name,width,height", VIEWPORTS)
class TestUIViewports:
    def _page(self, browser, width, height, runs):
        page = browser.new_page(viewport={"width": width, "height": height})
        page.set_content(render_dashboard(runs, PRICES))
        return page

    def test_renders_data(self, browser, name, width, height):
        page = self._page(browser, width, height, [FULL_RUN])
        assert _text(page, "input-tokens") == "130,808"
        assert _text(page, "output-tokens") == "65,404"
        assert _text(page, "compression-ratio") == "70.0%"
        assert _text(page, "cost-usd") == f"{FULL_RUN_COST:.6f}"
        assert page.locator('[data-testid="empty-state"]').count() == 0
        assert page.locator('[data-testid="cost-usd"]').is_visible()
        assert page.evaluate("document.documentElement.scrollWidth") <= width
        page.close()

    def test_renders_empty_state(self, browser, name, width, height):
        page = self._page(browser, width, height, [EMPTY_RUN])
        assert page.locator('[data-testid="empty-state"]').is_visible()
        assert "Sem métricas observadas" in _text(page, "empty-state")
        assert page.locator('[data-testid="savings-usd"]').count() == 0
        assert page.locator('[data-testid="tokens-saved"]').count() == 0
        assert page.evaluate("document.documentElement.scrollWidth") <= width
        page.close()
