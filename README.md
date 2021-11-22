# Github-Python

This is a Python utility to list commits for any open source project
This program helps in reading commit details and file strucutre of Open source code

## Instructions

Activate the virtual environment
```bash
Source ./gitpy/bin/activate
```

### List the commit information

```bash
python3 script.py remote_flag number_of_commits optional_repository_link repository_branch
```

**remote_flag:** Indicating whether the repo already exists on local machine or needs to be downloaded remotely [Set value as *'remote'* or *'local'*]\
**number_of_commits:** Number of commits to display and check information of\
**optional_repository_link:** Link to the remote repository if remote_flag set to true. If the remote_flag value is set to false, add the path to repository on local machine\
**repository_branch:** Repo branch to start iterating from

### List the number of authors

```
python3 author-name-script.py remote_flag number_of_commits optional_repository_link repository_branch >> Results/Autho_info/author_name_list.txt
```

### Get author information

```
python3 author-script.py remote_flag number_of_commits optional_repository_link repository_branch
```

### Run API GET commands

```
python3 github-api.py link_to_repo_API username personal_access_token
```

## Results

The results are stored inside the Results directory

1. **Commit_info:** This file contains information about the commits including hexcode, parents, number of updates and so on
2. **File_info:** This file contains information about number of commits per file
   **NOTE:** These results are dependent on the number of commits provide as command line argument.
3. **Author_name_list:** This file contains the list of the authors/contributors of a project or git repo
4. **Author_info.json:** This file contains links and contributions for individual authors
5. **Repo_info.json:** This file contains links to the API we can access to get information about authors, collaborators, commits, etc
