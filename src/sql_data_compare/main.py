import logging
import sys
from pathlib import Path

from dotenv import load_dotenv

from sql_data_compare.comparison import run_comparisons
from sql_data_compare.types import ComparisonConfig


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    try:
        # Load .env from current working directory if it exists
        load_dotenv(override=True)

        # Get project root (one level up from the module)
        project_root = Path(__file__).parent.parent.parent
        sql_dir = project_root / "sql"
        config_path = project_root / "config.json"

        # Ensure directories exist
        if not sql_dir.exists():
            raise FileNotFoundError(f"SQL directory not found: {sql_dir}")
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        # Load config and run comparisons
        config = ComparisonConfig(config_path, sql_dir)
        success = run_comparisons(config)

        return 0 if success else 1

    except Exception as e:
        logging.error(f"Fatal error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
