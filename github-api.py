import sys
import os

def main():
    repo_link = sys.argv[1]
    username = sys.argv[2]
    token = sys.argv[3]

    # Command to get the repository information
    repo_command = "curl " + repo_link + " >> Results/RESTAPITestResults/repo_info.json"
    os.system(repo_command)

    # Command to get author information
    author_command = "curl -u" + username + ":" + token + " " + repo_link + "/contributors >> Results/RESTAPITestResults/author_info.json"  
    os.system(author_command)

if __name__ == '__main__':
    main()