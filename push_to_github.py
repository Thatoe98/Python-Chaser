import os
import subprocess
import sys

def run_command(command):
    """Run a command and return its output"""
    try:
        result = subprocess.run(command, shell=True, check=True, 
                               capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e}")
        print(f"Error output: {e.stderr}")
        return None

def check_git_installed():
    """Check if Git is installed"""
    try:
        run_command("git --version")
        return True
    except:
        print("Git is not installed. Please install Git first.")
        return False

def initialize_repo():
    """Initialize Git repository if not already initialized"""
    if not os.path.exists(".git"):
        print("Initializing Git repository...")
        run_command("git init")
        print("Git repository initialized.")
    else:
        print("Git repository already initialized.")

def add_files():
    """Add all files to Git staging area"""
    print("Adding files to staging area...")
    run_command("git add .")
    print("Files added.")

def commit_changes(message="Initial commit of Python Chaser game"):
    """Commit changes to repository"""
    print("Committing changes...")
    run_command(f'git commit -m "{message}"')
    print("Changes committed.")

def add_remote(repo_url):
    """Add remote repository if not already added"""
    remotes = run_command("git remote -v")
    
    if remotes and "origin" in remotes:
        print("Remote 'origin' already exists. Updating URL...")
        run_command(f"git remote set-url origin {repo_url}")
    else:
        print("Adding remote repository...")
        run_command(f"git remote add origin {repo_url}")
    
    print("Remote repository configured.")

def push_to_github():
    """Push changes to GitHub"""
    print("Pushing to GitHub...")
    result = run_command("git push -u origin master")
    
    if not result:
        # Try main branch if master fails
        print("Trying 'main' branch instead...")
        result = run_command("git push -u origin main")
    
    if result:
        print("Successfully pushed to GitHub!")
    else:
        print("\nPush failed. You might need to:")
        print("1. Check your GitHub credentials")
        print("2. Ensure you have correct access to the repository")
        print("3. Run these commands manually:")
        print("   git push -u origin master")
        print("   or")
        print("   git push -u origin main")

def setup_github_credentials():
    """Setup GitHub credentials (basic)"""
    print("\nYou'll need to authenticate with GitHub.")
    print("You might be prompted for your GitHub username and password/token.")
    print("If you haven't set up a Personal Access Token, please create one at:")
    print("https://github.com/settings/tokens\n")
    
    input("Press Enter to continue...")

def main():
    repo_url = "https://github.com/Thatoe98/Python-Chaser.git"
    
    # Check if Git is installed
    if not check_git_installed():
        sys.exit(1)
    
    # Navigate to the project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    print(f"Working directory: {project_dir}")
    
    # Initialize repository
    initialize_repo()
    
    # Add files to staging
    add_files()
    
    # Commit changes
    commit_message = input("Enter commit message (default: 'Initial commit of Python Chaser game'): ")
    if not commit_message.strip():
        commit_message = "Initial commit of Python Chaser game"
    commit_changes(commit_message)
    
    # Setup GitHub authentication
    setup_github_credentials()
    
    # Add remote repository
    add_remote(repo_url)
    
    # Push to GitHub
    push_to_github()

if __name__ == "__main__":
    main()
