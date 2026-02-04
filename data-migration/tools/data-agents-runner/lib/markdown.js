function isoNow() {
  return new Date().toISOString();
}

function mdSection(title, bodyLines) {
  return [`## ${title}`, '', ...bodyLines, ''].join('\n');
}

function bullet(items) {
  return items.map((x) => `- ${x}`);
}

module.exports = { isoNow, mdSection, bullet };
