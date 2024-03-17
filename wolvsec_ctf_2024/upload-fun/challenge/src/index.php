<?php
    if($_SERVER['REQUEST_METHOD'] == "POST"){
        if ($_FILES["f"]["size"] > 1000) {
            echo "file too large";
            return;
        }

        if (str_contains($_FILES["f"]["name"], "..")) {
            echo "no .. in filename please";
            return;
        }

        if (empty($_FILES["f"])){
            echo "empty file";
            return;
        }

        $ip = $_SERVER['REMOTE_ADDR'];
        $flag = file_get_contents("/flag.txt");
        $hash = hash('sha256', $flag . $ip);

        if (move_uploaded_file($_FILES["f"]["tmp_name"], "./uploads/" . $hash . "_" . $_FILES["f"]["name"])) {
            echo "upload success";
        } else {
            echo "upload error";
        }
    } else {
        if (isset($_GET["f"])) {
            $path = "./uploads/" . $_GET["f"];
            if (str_contains($path, "..")) {
                echo "no .. in f please";
                return;
            }
            include $path;
        }

        highlight_file("index.php");
    }
?>
