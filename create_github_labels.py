#!/usr/bin/env python3

## @file create_github_labels.py
#  @brief A script to create GitHub issue labels.
#
#  @details This script creates a set of predefined labels in a GitHub repository.
#           It uses the GitHub API to post label data, which includes the label's
#           name, color, and description.
#
#           Key features:
#           - Configurable repository and owner.
#           - Secure token input using getpass.
#           - Predefined set of labels useful for issue tracking.
#
#  @code
#  Example interactive usage:
#  ```
#  $ python create_github_labels.py
#  Enter your GitHub username: [Your GitHub Username Here]
#  Enter your repository name: [Your Repository Name Here]
#  Enter your GitHub token: [Your GitHub Personal Access Token Here]
#  Successfully deleted label: bug
#  Successfully deleted label: enhancement
#  ...
#  Successfully created label: bug
#  Successfully created label: enhancement
#  ...
#  ```
#  @endcode
#
#  @note Ensure that the provided GitHub token has appropriate permissions for label creation.
#
#  @see GitHub API documentation for label creation.
#
#  @see https://github.com/Jekwwer/c-cpp-cmake-template for more details about the project.
#
#  @author Evgenii Shiliaev
#  @date December 04, 2023

import requests
from getpass import getpass


## @brief Deletes all existing labels from a GitHub repository.
#  @details This function retrieves all labels currently present in the specified GitHub repository
#           and deletes each one of them. It uses the GitHub API to fetch and delete labels.
#           For each label, a DELETE request is sent, and the function prints the status of each deletion attempt.
#
#  @param api_url The base URL of the GitHub API.
#  @param repo_owner The username of the owner of the GitHub repository.
#  @param repo_name The name of the repository from which to delete the labels.
#  @param headers Dictionary of API request headers for authentication and to specify the API version.
#
#  @pre The GitHub token used must have permissions to delete labels in the specified repository.
#  @pre Repository owner and name must be correctly configured.
#
#  @post All existing labels in the specified repository are deleted.
#
#  @note This function is useful for label management and preventing conflicts when creating new labels.
#
#  @warning Ensure that the GitHub token is kept secure and not logged or displayed.
#
#  @todo Consider handling network errors and unauthorized access more gracefully.
def delete_existing_labels(api_url, repo_owner, repo_name, headers):
    response = requests.get(
        f"{api_url}/repos/{repo_owner}/{repo_name}/labels", headers=headers
    )
    if response.status_code == 200:
        existing_labels = response.json()
        for label in existing_labels:
            delete_response = requests.delete(
                f"{api_url}/repos/{repo_owner}/{repo_name}/labels/{label['name']}",
                headers=headers,
            )
            if delete_response.status_code == 204:
                print(f"Successfully deleted label: {label['name']}")
            else:
                print(
                    f"Failed to delete label: {label['name']} - {delete_response.content}"
                )


## @brief Creates a set of predefined labels in a GitHub repository.
#  @details This function iterates through a list of label definitions and creates each label in the specified GitHub repository.
#           Each label is defined by its name, color, and description. The GitHub API is used to create these labels.
#           The function prints out the status of each label creation attempt.
#
#  @param labels_to_create A list of dictionaries, each dictionary containing the 'name', 'color', and 'description' for a label.
#
#  @pre The GitHub token used must have permissions to create labels in the specified repository.
#  @pre Repository owner and name must be correctly configured.
#
#  @post Labels are created in the specified repository, unless an error occurs.
#
#  @note This function does not handle label creation conflicts (existing labels with the same name).
#
#  @warning Ensure that the GitHub token is kept secure and not logged or displayed.
#
#  @code
#  create_labels(labels_to_create)
#  @endcode
#
#  @todo Implement error handling for network issues and unauthorized access.
def create_labels(api_url, repo_owner, repo_name, headers, labels_to_create):
    for label in labels_to_create:
        response = requests.post(
            f"{api_url}/repos/{repo_owner}/{repo_name}/labels",
            headers=headers,
            json=label,
        )
        if response.status_code == 201:
            print(f"Successfully created label: {label['name']}")
        else:
            print(f"Failed to create label: {label['name']} - {response.content}")


## @mainpage
#  @brief Entry point for the script execution.
#
#  @details This block executes when the script is run directly.
#           It prompts the user for their GitHub username, repository name, and token.
#           Then it proceeds to delete all existing labels and create new ones as specified.
#
if __name__ == "__main__":
    # Configuration
    api_url = "https://api.github.com"
    # Prompt user for GitHub username
    repo_owner = input("Enter your GitHub username: ")
    # Prompt user for repository name
    repo_name = input("Enter your repository name: ")
    token = getpass("Enter your GitHub token: ")  # Securely get user's token

    # Headers to authenticate and to use the API version that supports label descriptions
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    # List of labels to create
    labels_to_create = [
        {
            "name": "bug",
            "color": "d73a4a",
            "description": "Indicates a problem that impairs or prevents the functions of the product",
        },
        {
            "name": "dependencies",
            "color": "0366d6",
            "description": "Concerns outdated, broken, or problematic dependencies",
        },
        {
            "name": "documentation",
            "color": "0075ca",
            "description": "Relates to improvements or additions to documentation",
        },
        {
            "name": "duplicate",
            "color": "cfd3d7",
            "description": "Signals an issue that has already been reported, often with a reference to the original",
        },
        {
            "name": "enhancement",
            "color": "a2eeef",
            "description": "Suggests a new feature or improvement to existing functionality",
        },
        {
            "name": "environment",
            "color": "f9d0c4",
            "description": "Involves issues related to the project's development, testing, or production environment",
        },
        {
            "name": "good first issue",
            "color": "7057ff",
            "description": "Suitable for first-time contributors, these issues are a great way to get involved",
        },
        {
            "name": "help wanted",
            "color": "008672",
            "description": "Requests assistance from the community or team members for an issue or initiative",
        },
        {
            "name": "invalid",
            "color": "e4e669",
            "description": "Marks an issue that is no longer relevant or that has been filed incorrectly",
        },
        {
            "name": "performance",
            "color": "fbca04",
            "description": "Highlights areas of the codebase that could be optimized for speed and efficiency",
        },
        {
            "name": "question",
            "color": "d876e3",
            "description": "Seeks further information or clarification on a topic or issue",
        },
        {
            "name": "refactor",
            "color": "1d76db",
            "description": "Suggests improvements for code organization or architecture without altering behavior",
        },
        {
            "name": "security",
            "color": "b60205",
            "description": "Concerns or reports related to security vulnerabilities",
        },
        {
            "name": "test-case",
            "color": "5319e7",
            "description": "Indicates missing tests or proposes new ones for better coverage",
        },
        {
            "name": "user-story",
            "color": "c2e0c6",
            "description": "Describes a software feature from an end-user perspective, focusing on their needs and experiences",
        },
        {
            "name": "violation",
            "color": "e11d21",
            "description": "Pertains to vulnerabilities that could impact the security of the project",
        },
        {
            "name": "wontfix",
            "color": "000000",
            "description": "Acknowledges an issue that the project has decided not to address at the present time",
        },
    ]

# Delete all existing labels before creating new ones
delete_existing_labels(api_url, repo_owner, repo_name, headers)

# Create new labels
create_labels(api_url, repo_owner, repo_name, headers, labels_to_create)

# End of create_github_labels.py
