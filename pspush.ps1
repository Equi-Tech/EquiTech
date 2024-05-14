# Function to check if Commitizen is installed
function Check-Commitizen {
    if (-not (Get-Command commitizen-go -ErrorAction SilentlyContinue)) {
        Write-Error "Commitizen Not Found!"
        exit 1
    }
}

# Branch name
$BRANCH = "master"  # or 'main'/'development'

# Function to push changes to Git
function Push-Changes {
    git add .
    git cz
    git push origin -u $BRANCH
}

# Main function
function Main {
    Check-Commitizen
    Push-Changes
}

Main
