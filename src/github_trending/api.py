from github_trending import init as call_github_trending

def __init__():
    trending = call_github_trending()

    print(trending)

__init__()