# Data Validation Framework
# Databricks Delta Table Validation
# Generated: 2026-06-16

from pyspark.sql import SparkSession
from pyspark.sql.functions import count, col, when
import logging

logger = logging.getLogger(__name__)

class DatabricksValidation:
    def __init__(self):
        self.spark = SparkSession.builder.appName("databricks-validation").getOrCreate()
        self.validation_results = []
    
    def validate_row_count(self, table_name, expected_min_records):
        """Validate minimum row count."""
        df = self.spark.table(table_name)
        actual_count = df.count()
        
        result = {
            'table': table_name,
            'check': 'row_count',
            'expected_min': expected_min_records,
            'actual': actual_count,
            'status': 'PASS' if actual_count >= expected_min_records else 'FAIL'
        }
        
        self.validation_results.append(result)
        logger.info(f"{result['check']} - {table_name}: {result['status']} ({actual_count} records)")
        return result
    
    def validate_schema(self, table_name, expected_columns):
        """Validate table schema."""
        df = self.spark.table(table_name)
        actual_columns = set(df.columns)
        expected_set = set(expected_columns)
        
        missing = expected_set - actual_columns
        status = 'PASS' if len(missing) == 0 else 'FAIL'
        
        result = {
            'table': table_name,
            'check': 'schema',
            'expected_columns': expected_columns,
            'actual_columns': df.columns,
            'missing_columns': list(missing),
            'status': status
        }
        
        self.validation_results.append(result)
        logger.info(f"schema - {table_name}: {status}")
        return result
    
    def validate_nulls(self, table_name, non_nullable_columns):
        """Validate no unexpected nulls."""
        df = self.spark.table(table_name)
        
        null_counts = {}
        for col_name in non_nullable_columns:
            null_count = df.where(col(col_name).isNull()).count()
            null_counts[col_name] = null_count
        
        status = 'PASS' if all(v == 0 for v in null_counts.values()) else 'FAIL'
        
        result = {
            'table': table_name,
            'check': 'null_values',
            'null_counts': null_counts,
            'status': status
        }
        
        self.validation_results.append(result)
        logger.info(f"null_values - {table_name}: {status}")
        return result
    
    def validate_duplicates(self, table_name, key_columns):
        """Validate no duplicate keys."""
        df = self.spark.table(table_name)
        
        deduped = df.groupBy(key_columns).count().where(col('count') > 1)
        duplicate_count = deduped.count()
        
        status = 'PASS' if duplicate_count == 0 else 'FAIL'
        
        result = {
            'table': table_name,
            'check': 'duplicates',
            'key_columns': key_columns,
            'duplicate_count': duplicate_count,
            'status': status
        }
        
        self.validation_results.append(result)
        logger.info(f"duplicates - {table_name}: {status} ({duplicate_count} dups)")
        return result
    
    def run_all_validations(self):
        """Execute all validation checks."""
        logger.info("Starting validation suite")
        
        # Rentabilidade Diaria Validations
        self.validate_row_count(
            'rentabilidade.raw.tb_rentabilidade_diaria',
            expected_min_records=450000000
        )
        
        self.validate_schema(
            'rentabilidade.raw.tb_rentabilidade_diaria',
            expected_columns=['data_calculo', 'id_cliente', 'rentabilidade', 'comissao']
        )
        
        self.validate_nulls(
            'rentabilidade.raw.tb_rentabilidade_diaria',
            non_nullable_columns=['data_calculo', 'id_cliente', 'rentabilidade']
        )
        
        self.validate_duplicates(
            'rentabilidade.raw.tb_rentabilidade_diaria',
            key_columns=['data_calculo', 'id_cliente']
        )
        
        # Rentabilidade Consolidada Validations
        self.validate_row_count(
            'rentabilidade.processed.tb_rentabilidade_consolidada',
            expected_min_records=9000000
        )
        
        # Summary
        passed = sum(1 for r in self.validation_results if r['status'] == 'PASS')
        failed = sum(1 for r in self.validation_results if r['status'] == 'FAIL')
        
        logger.info(f"Validation Complete: {passed} passed, {failed} failed")
        
        return {
            'total': len(self.validation_results),
            'passed': passed,
            'failed': failed,
            'results': self.validation_results
        }

if __name__ == "__main__":
    validator = DatabricksValidation()
    results = validator.run_all_validations()
    exit(0 if results['failed'] == 0 else 1)
