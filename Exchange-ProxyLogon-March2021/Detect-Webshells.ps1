# Simple script to look for recently written .aspx files which could indicate the presence of a webshell
# Version 1.0

# Author Tom Quinn - https://twitter.com/tomquinn8


# Days to search
$days = 10

# Look for .aspx files written to in the last x days
write-host "Searching for .aspx files written in the last $days days..."
[array]$files=@()
$files = Get-ChildItem -Path 'C:\' -Filter *.aspx -Recurse -ErrorAction SilentlyContinue | ? {$_.LastWriteTime -gt (Get-Date).AddDays(-$days)}

if($files.count -gt 0) {
    write-host "Suspiscous files found! The following should be reviewed manually:" -ForegroundColor Red
    foreach ($file in $files) {
        write-host "    "$file.fullname -ForegroundColor Red
    }
}
else {
    write-host "No .aspx files found which have been written to in the last $days days." -ForegroundColor Green
}
