import os
import re
import json

def parse_plugins_from_gradle(file_path):
    """
    Parses a Gradle file to extract plugins and maps them as package entities.

    Args:
        file_path (str): Path to the Gradle file.

    Returns:
        list: A list of package entities formatted for Port's BULK_UPSERT.
    """
    entities = []

    # Regex to match plugin declarations
    plugin_pattern = re.compile(r"id\s+['\"]([^'\"]+)['\"]\s+version\s+['\"]([^'\"]+)['\"]")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            matches = plugin_pattern.findall(content)

            for plugin, version in matches:
                entities.append({
                    "identifier": plugin,
                    "blueprint": "package",
                    "properties": {
                        "package": plugin,
                        "version": version
                    }
                })

    except FileNotFoundError:
        print(f"Error: Gradle file not found at {file_path}")
    except Exception as e:
        print(f"Error parsing file: {e}")

    return entities

def create_service_entity(repo_name, dependencies):
    """
    Creates a service entity and connects it to its dependencies.

    Args:
        repo_name (str): The repository name (without the organization).
        dependencies (list): A list of dependency identifiers.

    Returns:
        dict: A service entity formatted for Port's BULK_UPSERT.
    """
    return {
        "identifier": repo_name,
        "blueprint": "service",
        "relations": {
            "dependencies": dependencies  # Array of dependency identifiers
        }
    }

def main():
    gradle_path = os.getenv("GRADLE_PATH")
    if not gradle_path:
        raise ValueError("GRADLE_PATH environment variable is not set.")

    # Parse the Gradle file
    dependencies = parse_plugins_from_gradle(gradle_path)

    # Extract the repository name from GITHUB_REPOSITORY (e.g., org/repo -> repo)
    full_repo_name = os.getenv("GITHUB_REPOSITORY", "org/default-repo")
    repo_name = full_repo_name.split("/")[-1]

    # Collect dependency identifiers for relations
    dependency_ids = [dep["identifier"] for dep in dependencies]

    # Create the service entity
    service_entity = create_service_entity(repo_name, dependency_ids)

    # Combine service entity and dependencies
    all_entities = [service_entity] + dependencies

    # Output the result in JSON format for Port
    print(json.dumps(all_entities, indent=2))

if __name__ == "__main__":
    main()
