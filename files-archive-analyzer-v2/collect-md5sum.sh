# Define the output file

# Check if the output filename was provided
if [ -z "$1" ]; then
    echo "Error: Missing output filename."
    echo "Usage: $0 <output_file.tsv> <optional:destination folder, default - current>"
    exit 1
fi

output="$1"

if [ -z "$2" ]; then
    destination_folder="."
else
    destination_folder=$2
fi


# Add a header to the TSV
# echo -e "Path\tFilename\tMD5Sum" > "$output"

# Find files and process them
find $destination_folder -type f -print0 | while IFS= read -r -d '' file; do
    # Get the MD5 hash
    md5=$(md5sum "$file" | awk '{print $1}')
    
    # Get the directory path
    path=$(dirname "$file")
    
    # Get the filename
    basename=$(basename "$file")
    
    # Append to the TSV file
    echo -e "$md5\t$basename\t$path" >> "$output"
done

echo "Done! Data saved to $output"
