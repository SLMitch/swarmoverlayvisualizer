<?php
    $db = new PDO('mysql:host=mariadb;dbname=swarmoverlayvisualizer;charset=utf8mb4', 'root', 'swarmoverlayvisualizer');
    
    $dockerapihost = $_GET['host'].":2375"; //location of Docker Swarm API, change to yours
?>