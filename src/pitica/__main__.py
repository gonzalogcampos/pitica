if __name__ == "__main__":
    import os
    import argparse
    import logging
    from pitica.generator.generate_sources import generate_sources

    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(description='Pitica generate sources.')
    parser.add_argument('-d', dest='directory',
                        type=str, help='Root directory')
    parser.add_argument('-c', dest='clean',
                        action='store_true', help='Clean root directory')
    args = parser.parse_args()

    directory = args.directory
    clean = args.clean

    if not directory:
        directory = "."

    if not os.path.isabs(directory):
        directory = os.path.join(os.getcwd(), directory)

    if not directory and not clean:
        logger.error("Usage: -d <directory> -c")
        exit(1)

    generate_sources(directory, clean)
