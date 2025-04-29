# GitHub Trending

A Python package that allows you to fetch trending repositories from GitHub. This tool scrapes the GitHub trending page and provides structured data about trending repositories.

## Features

- Fetch trending repositories from GitHub
- Filter by date (daily, weekly, monthly)
- Get repository details including:
  - Repository name
  - Link
  - Description
  - Programming language
  - Star count

## Installation

This project uses Poetry for dependency management. Make sure you have Python 3.13 or higher installed.

1. Clone the repository:
```bash
git clone https://github.com/leodo9x/github-trending.git
cd github-trending
```

2. Install dependencies using Poetry:
```bash
poetry install
```

## Usage

Here's a simple example of how to use the package:

```python
from github_trending import init

# Get today's trending repositories
trending_repos = init()

# Get weekly trending repositories
weekly_trending = init(date='weekly')

# Get monthly trending repositories
monthly_trending = init(date='monthly')

# Print repository information
for repo in trending_repos:
    print(f"Name: {repo['name']}")
    print(f"Link: {repo['link']}")
    print(f"Description: {repo['description']}")
    print(f"Language: {repo['language']}")
    print(f"Stars: {repo['star']}")
    print("---")
```

## Dependencies

- Python >= 3.13
- requests >= 2.32.3
- beautifulsoup4 >= 4.13.4

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
