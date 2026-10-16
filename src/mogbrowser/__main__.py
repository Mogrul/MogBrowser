import asyncio

from mogbrowser import App, config, load_logger


def main():
    app = App()
    load_logger(config.debug)
    asyncio.run(app.run_task(
        host="0.0.0.0",
        port=5000,
        debug=True,
    ))

if __name__ == "__main__":
    main()