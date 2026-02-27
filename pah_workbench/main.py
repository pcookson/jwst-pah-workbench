"""Application entrypoint."""

def main() -> int:
    from pah_workbench.app import run

    return run()


if __name__ == "__main__":
    raise SystemExit(main())
