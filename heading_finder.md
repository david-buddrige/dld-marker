You can run the heading_finder.md with a powershell command like so:

```
Get-ChildItem -Recurse "C:\Users\5004031\OneDrive - TAFE\2025-semester-2\Cluster - Digital Layout and Design\marking\at2\at2-20250926" -Filter *.html | ForEach-Object { python .\heading_finder.py -html-file $_.FullName } > check-headings.txt
```

This will loop through a set of directories starting from the one specified, and find any html 
files and run the command against it.

