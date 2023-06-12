<html>
<head>       
       <title>Dernières Sorties</title>       
       <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />                                   
</head>
<body>   
    <hr>
    <a href='http://www.tchok.com'><img src='images/150_club-des-cent-cols.png'> </a>
    <hr>    
    <?php     
        require_once 'sqldb.php';
        include 'functions.php';

        if (isset($_GET['id_strava_activity'])){        
            $id_strava_activity = $_GET['id_strava_activity'];        
        }

        if (isset($_GET['access_token'])){        
            $access_token = $_GET['access_token'];        
        }
                
        $pointList = getActivityStreams( $id_strava_activity,$access_token);
                    
        $allCols = returnColList ();
        $i = 0;
                
        foreach ($pointList as $value) {            
            $latPoint = $value[0];
            $lonPoint = $value[1];

            foreach ($allCols as $valueCol) {            
                $nomCol = $valueCol[0];
                $lonCol = $valueCol[1];
                $latCol = $valueCol[2];
                $altCol = $valueCol[3];
                
                $distance = distance($latCol,$lonCol,$latPoint , $lonPoint,"K");   
                //echo $nomCol . "/ Lat = ".  $latPoint . "/ Lon =  ". $lonPoint . "/". $distance . "</br>";

                                
                if ($distance < 0.05) {                      
                    //echo $nomCol ."/". $lonCol ."/". $latCol ."/". $latPoint ."/". $lonPoint ."/".  $distance . "</br>";
                    //echo $nomCol . "/".  $distance . "</br>";
                    $colOk[$i] = $nomCol;        
                    $i++;
                }
            }

        }

        

       $colActivity = array_unique($colOk);
        
        foreach ($colActivity as $value) {            
            echo $value. "</br>";            
        }
        

                                       
    ?>    
</body>
</html>    



