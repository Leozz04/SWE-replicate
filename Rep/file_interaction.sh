# @yaml
# signature: search_dir <search_term> [<dir>]
# docstring: searches for search_term in all files in dir. If dir is not provided, searches in the current directory
# arguments:
#   search_term:
#     type: string
#     description: the term to search for
#     required: true
#   dir:
#     type: string
#     description: the directory to search in (if not provided, searches in the current directory)
#     required: false
search_dir() {
    if [ $# -eq 1 ]; then
        local search_term="$1"
        local dir="./"
    elif [ $# -eq 2 ]; then
        local search_term="$1"
        if [ -d "$2" ]; then
            local dir="$2"
        else
            echo "Directory $2 not found"
            return
        fi
    else
        echo "Usage: search_dir <search_term> [<dir>]"
        return
    fi
    dir=$(realpath "$dir")
    local matches=$(find "$dir" -type f ! -path '*/.*' -exec grep -nIH -- "$search_term" {} + | cut -d: -f1 | sort | uniq -c)
    # if no matches, return
    if [ -z "$matches" ]; then
        echo "No matches found for \"$search_term\" in $dir"
        return
    fi
    # Calculate total number of matches
    local num_matches=$(echo "$matches" | awk '{sum+=$1} END {print sum}')
    # calculate total number of files matched
    local num_files=$(echo "$matches" | wc -l | awk '{$1=$1; print $0}')
    # if num_files is > 100, print an error
    if [ $num_files -gt 100 ]; then
        echo "More than $num_files files matched for \"$search_term\" in $dir. Please narrow your search."
        return
    fi

    echo "Found $num_matches matches for \"$search_term\" in $dir:"
    echo "$matches" | awk '{$2=$2; gsub(/^\.+\/+/, "./", $2); print $2 " ("$1" matches)"}'
    echo "End of matches for \"$search_term\" in $dir"
}

# @yaml
# signature: search_file <search_term> [<file>]
# docstring: searches for search_term in file. If file is not provided, searches in the current open file
# arguments:
#   search_term:
#     type: string
#     description: the term to search for
#     required: true
#   file:
#     type: string
#     description: the file to search in (if not provided, searches in the current open file)
#     required: false
search_file() {
    # Check if the first argument is provided
    if [ -z "$1" ]; then
        echo "Usage: search_file <search_term> [<file>]"
        return
    fi
    # Check if the second argument is provided
    if [ -n "$2" ]; then
        # Check if the provided argument is a valid file
        if [ -f "$2" ]; then
            local file="$2"  # Set file if valid
        else
            echo "Usage: search_file <search_term> [<file>]"
            echo "Error: File name $2 not found. Please provide a valid file name."
            return  # Exit if the file is not valid
        fi
    else
        # Check if a file is open
        if [ -z "$CURRENT_FILE" ]; then
            echo "No file open. Use the open command first."
            return  # Exit if no file is open
        fi
        local file="$CURRENT_FILE"  # Set file to the current open file
    fi
    local search_term="$1"
    file=$(realpath "$file")
    # Use grep to directly get the desired formatted output
    local matches=$(grep -nH -- "$search_term" "$file")
    # Check if no matches were found
    if [ -z "$matches" ]; then
        echo "No matches found for \"$search_term\" in $file"
        return
    fi
    # Calculate total number of matches
    local num_matches=$(echo "$matches" | wc -l | awk '{$1=$1; print $0}')

    # calculate total number of lines matched
    local num_lines=$(echo "$matches" | cut -d: -f1 | sort | uniq | wc -l | awk '{$1=$1; print $0}')
    # if num_lines is > 100, print an error
    if [ $num_lines -gt 100 ]; then
        echo "More than $num_lines lines matched for \"$search_term\" in $file. Please narrow your search."
        return
    fi

    # Print the total number of matches and the matches themselves
    echo "Found $num_matches matches for \"$search_term\" in $file:"
    echo "$matches" | cut -d: -f1-2 | sort -u -t: -k2,2n | while IFS=: read -r filename line_number; do
        echo "Line $line_number:$(sed -n "${line_number}p" "$file")"
    done
    echo "End of matches for \"$search_term\" in $file"
}

# @yaml
# signature: find_file <file_name> [<dir>]
# docstring: finds all files with the given name in dir. If dir is not provided, searches in the current directory
# arguments:
#   file_name:
#     type: string
#     description: the name of the file to search for
#     required: true
#   dir:
#     type: string
#     description: the directory to search in (if not provided, searches in the current directory)
#     required: false
find_file() {
    if [ $# -eq 1 ]; then
        local file_name="$1"
        local dir="./"
    elif [ $# -eq 2 ]; then
        local file_name="$1"
        if [ -d "$2" ]; then
            local dir="$2"
        else
            echo "Directory $2 not found"
            return
        fi
    else
        echo "Usage: find_file <file_name> [<dir>]"
        return
    fi

    dir=$(realpath "$dir")
    local matches=$(find "$dir" -type f -name "$file_name")
    # if no matches, return
    if [ -z "$matches" ]; then
        echo "No matches found for \"$file_name\" in $dir"
        return
    fi
    # Calculate total number of matches
    local num_matches=$(echo "$matches" | wc -l | awk '{$1=$1; print $0}')
    echo "Found $num_matches matches for \"$file_name\" in $dir:"
    echo "$matches" | awk '{print $0}'
}
open() {
    if [ -z "$1" ]
    then
        echo "Usage: open <file>"
        return
    fi
    # Check if the second argument is provided
    if [ -n "$2" ]; then
        # Check if the provided argument is a valid number
        if ! [[ $2 =~ ^[0-9]+$ ]]; then
            echo "Usage: open <file> [<line_number>]"
            echo "Error: <line_number> must be a number"
            return  # Exit if the line number is not valid
        fi
        local max_line=$(awk 'END {print NR}' $1)
        if [ $2 -gt $max_line ]; then
            echo "Warning: <line_number> ($2) is greater than the number of lines in the file ($max_line)"
            echo "Warning: Setting <line_number> to $max_line"
            local line_number=$(jq -n "$max_line")  # Set line number to max if greater than max
        elif [ $2 -lt 1 ]; then
            echo "Warning: <line_number> ($2) is less than 1"
            echo "Warning: Setting <line_number> to 1"
            local line_number=$(jq -n "1")  # Set line number to 1 if less than 1
        else
            local OFFSET=$(jq -n "$WINDOW/6" | jq 'floor')
            local line_number=$(jq -n "[$2 + $WINDOW/2 - $OFFSET, 1] | max | floor")
        fi
    else
        local line_number=$(jq -n "$WINDOW/2")  # Set default line number if not provided
    fi

    if [ -f "$1" ]; then
        export CURRENT_FILE=$(realpath $1)
        export CURRENT_LINE=$line_number
        _constrain_line
        _print
    elif [ -d "$1" ]; then
        echo "Error: $1 is a directory. You can only open files. Use cd or ls to navigate directories."
    else
        echo "File $1 not found"
    fi
}

# @yaml
# signature: goto <line_number>
# docstring: moves the window to show <line_number>
# arguments:
#   line_number:
#     type: integer
#     description: the line number to move the window to
#     required: true
goto() {
    if [ $# -gt 1 ]; then
        echo "goto allows only one line number at a time."
        return
    fi
    if [ -z "$CURRENT_FILE" ]
    then
        echo "No file open. Use the open command first."
        return
    fi
    if [ -z "$1" ]
    then
        echo "Usage: goto <line>"
        return
    fi
    if ! [[ $1 =~ ^[0-9]+$ ]]
    then
        echo "Usage: goto <line>"
        echo "Error: <line> must be a number"
        return
    fi
    local max_line=$(awk 'END {print NR}' $CURRENT_FILE)
    if [ $1 -gt $max_line ]
    then
        echo "Error: <line> must be less than or equal to $max_line"
        return
    fi
    local OFFSET=$(jq -n "$WINDOW/6" | jq 'floor')
    export CURRENT_LINE=$(jq -n "[$1 + $WINDOW/2 - $OFFSET, 1] | max | floor")
    _constrain_line
    _print
}