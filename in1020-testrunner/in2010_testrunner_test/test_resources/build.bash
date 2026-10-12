zipdir() {
	filename="$(realpath "$1.zip")"
	(cd "$1"; zip "$filename" -r .)
}

zipdir test_oblig

ls *.zip > index.txt
