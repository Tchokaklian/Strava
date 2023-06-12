<?php  
    
    // Connexion

    function OpenConnexion(){

        $dbHost = 'tchokcommcdbo100.mysql.db';
        $dbBase = 'tchokcommcdbo100';
        $dbUser = 'tchokcommcdbo100';
        $dbPassword = 'Sarkis19';


         /*** msqli procédural ***/
        $mysqli = mysqli_connect( $dbHost, $dbUser, $dbPassword, $dbBase );

        if ( mysqli_connect_errno( $mysqli ) ) {
            echo "Échec connexion mysqli_connect : " . mysqli_connect_error() . "<br>\n";
        } else {
            // echo "Connected to mysqli_connect : " . mysqli_connect_error() . "<br>\n";
            return $mysqli;
        }

    }

    /////////////////////////////////////////
    //          Liste des Cols
    /////////////////////////////////////////
    
    function getListeCols($filter) {
        
        
        $conn = OpenConnexion();
        
        echo "<B><U>Liste des cols cyclables des Alpes Maritimes</B></U> ". "<br>";

        $sql = 'SELECT col_nom, col_alt FROM col WHERE col_code like "%' .$filter. '%" order by col_alt' ;
        $result = $conn->query($sql);       

        if ($result->num_rows > 0) {                            
            $i = 0;
            #-----------------------------------
            echo '<table style="width:500px">';
            echo "<tr>";
              echo "<th>Num</th>";
              echo "<th>Col</th>";
              echo "<th>Altitude</th>";                              
            echo"</tr>";
            #-----------------------------------
            // output data of each row
            while($row = $result->fetch_assoc()) {
                   $i++;       
                   $col_nom = $row[col_nom];                            
                   $col_alt = $row[col_alt];                                  
                   echo "<tr>";
                   echo "<td>" . $i . "</td>";
                   echo "<td>" . utf8_encode($col_nom) . "</td>";
                   echo "<td>" . $col_alt . "</td>";
                   echo "</tr>";
            }                            
          echo "</table>";                          
        } else {
            echo "0 results";
        }

        $conn->close();  
           
    }              
    

    /////////////////////////////////////////
    //          New Strava User
    /////////////////////////////////////////

    function addStravaUser($token_type,$access_token,$expires_at,$refresh_token,$athlete_id,$first_name,$last_name,$city,$country,$sex,$strava_email,$codeClient){        
        $conn = OpenConnexion();

        $delsql = "DELETE FROM strava_user WHERE athlete_id='" . $athlete_id . "'";
        if ($conn->query($delsql) === TRUE) {
            #echo "Record deleted successfully";
            $sql = "INSERT INTO strava_user (first_name,last_name,token_type,access_token,refresh_token,expires_at,athlete_id,city,country,sex,email,client_code ) ";
            $sql = $sql. "VALUES ($first_name,$last_name,$token_type,$access_token,$refresh_token,$expires_at,$athlete_id,$city,$country,$sex,$strava_email,$codeClient)";
        
            if ($conn->query($sql) === TRUE) {
                echo "Vous êtes bien enregistré dans la base des 100 cols !";
            } else {
                echo "Error: " . $sql . "<br>" . $conn->error;
            }
        } else {
            echo "Error deleting record: " . mysqli_error($conn);
        }

        $conn->close(); 
        
        
    }
    
    

    /////////////////////////////////////////
    //          Refresh Token
    /////////////////////////////////////////
    

    function refreshToken($email,$password){
        
        $conn = OpenConnexion();

        $sql = "SELECT first_name, last_name, access_token, refresh_token, athlete_id, client_code, expires_at FROM strava_user ";
        $sql = $sql. "WHERE email = '" . $email . "' AND password = '" . $password . "'";

        #echo $sql ;
        
        $result = $conn->query($sql);

        if ($result->num_rows == 1) {
            
            while($row = $result->fetch_assoc()) {
                $first_name = $row["first_name"];
                $last_name = $row["last_name"];
                $access_token = $row["access_token"];
                $refresh_token = $row["refresh_token"];
                $athlete_id = $row["athlete_id"];
                $client_code = $row["client_code"];
                $expires_at = $row["expires_at"];
                
                $url = 'https://www.strava.com/api/v3/oauth/token';
                $curl = curl_init($url);

                curl_setopt($curl, CURLOPT_POST, true);
                curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);

                # 2711 = Mon application
                $data = "client_id=2711&client_secret=144e2d05e4b1b91f095dbafe6b40fbc4a9d0933e&grant_type=refresh_token&refresh_token=".$refresh_token;
    
                curl_setopt($curl, CURLOPT_POSTFIELDS, $data);

                $result = curl_exec($curl);
    
                curl_close($curl);
                
                ##########################
                #  print $result;
                ##########################

                $jsonArrayResponse = json_decode($result);
    
                $access_token = $jsonArrayResponse-> access_token;
                $expires_at = $jsonArrayResponse-> expires_at;
                
                $sql = "UPDATE strava_user SET access_token ='" . $access_token . "', expires_at = ". $expires_at . " WHERE email = '" . $email . "' AND password = '" . $password . "'";

                # echo "----------------> upd=". $sql;

                if ($conn->query($sql) === TRUE) {
                    echo "<p>Token updated, please reload your page ...";                                        
                    echo "<a href='http://www.tchok.com/'>Reload</a>.";
                    echo"</p>";
                    }
                else{
                    echo "Error update Token ...";
                }

            }
                       
            $conn->close();  

            return $access_token;
        
        }   
    }


    /////////////////////////////////////////
    //      getListActivities
    /////////////////////////////////////////

    function getListActivities($email,$password,$period){

        //$ http GET "https://www.strava.com/api/v3/athlete/activities?before=&after=&page=&per_page=" "Authorization: Bearer [[token]]"
                
        $conn = OpenConnexion();

        $sql = "SELECT access_token, athlete_id, expires_at FROM strava_user ";
        $sql = $sql. "WHERE email = '" . $email . "' AND password = '" . $password . "'";

        $result = $conn->query($sql);

        #echo $sql ;
        
        $result = $conn->query($sql);

        if ($result->num_rows > 0) {            

            while($row = $result->fetch_assoc()) {               
                $access_token = $row["access_token"];     
                $athlete_id = $row["athlete_id"];                
                $expires_at = $row["expires_at"];                 
            }                

            $myEpch = time();
            
            if ( $expires_at - $myEpch < 0  )                            
                $access_token = refreshToken($email,$password );
            

            if ( $period == "1M" ) {
                $after = $myEpch - 2678400; 
            }

            if ( $period == "3M" ) {
                $after = $myEpch - 8035200;
            }

            if ( $period == "6M" ) {
                $after = $myEpch - 16070400;
            }

            if ( $period == "1Y" ) {
                $after = $myEpch - 31622400;
            }

            //$after = $myEpch - 2678400;
                        
            for($page = 1; $page <= 10; $page++){    
                $url = "https://www.strava.com/api/v3/athlete/activities?access_token=".$access_token."&page=".$page."&after=" . $after;                    

                $curl = curl_init($url);
            
                curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
                curl_setopt($ch, CURLOPT_HEADER, 0);

                $result = curl_exec($curl);
                        
                curl_close($curl);
                                    
                $jsonArrayResponse = json_decode($result);
                //echo var_dump($jsonArrayResponse) . "<br>";

                foreach ($jsonArrayResponse as $activiy){
                    $name = $activiy-> name;
                    $name = addslashes($name);
                    $name = utf8_decode($name);
                    $distance = $activiy-> distance;
                    $id = $activiy-> id;
                    $deniv = $activiy-> total_elevation_gain;
                    $sport = $activiy-> type;                
                    $start_date = $activiy-> start_date_local;
                    #$start_date = substr($start_date,0,10);
                    $country = $activiy-> location_country;
                        
                    $sqldel = "DELETE FROM activity WHERE id_strava_activity=" . $id;
                    
    
                    if ($conn->query($sqldel) === TRUE) {
                        #echo "Del/Ins ... ". "</br>";
                    } else {
                        echo "Error: " . $sqldel . " // " . $conn->error;   
                    }
                    
                                
                    $sql = "INSERT INTO activity (id_strava_activity,id_strava_athlete,	activity_name,	activity_distance,	activity_elevation,	activity_sport, activity_date, country) ";
                    $sql = $sql. "VALUES (" . $id . "," . $athlete_id. ",'". $name. "', ". $distance. ",". $deniv. ",'" .$sport. "','" . $start_date . "','" . $country . "')";
                                     
                    if ($conn->query($sql) === TRUE) {
                        //echo "Enregistrement des Activités réalisé avec succès". "</br>";
                    } else {
                        echo "Error: " . $sql . " // " . $conn->error;
                    }
    
            
                }
    

                
            }


            displayListActivities($athlete_id,$access_token);
                
        }   else {
            echo " Login / Mot de passe invalides ....";                 
        }

        $conn->close();  
    
    }

    ///////////////////////////////////////////////////////

    function getActivityStreams($activity_id, $access_token){        
        // "https://www.strava.com/api/v3/activities/{id}/streams?keys=&key_by_type=" "Authorization: Bearer [[token]]"
        
        $url = "https://www.strava.com/api/v3/activities/" .$activity_id. "/streams?access_token=".$access_token."&keys=latlng" ;
        $curl = curl_init($url);
                
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HEADER, 0);
                    
        $result = curl_exec($curl);
                
        curl_close($curl);

        //echo $result;        
        $jsonArrayResponse = json_decode($result);
        
        $stream = $jsonArrayResponse[0];
        $latlng = $stream-> data; 

        $i=0;
              
        foreach( $latlng as $value ) {
            $lat = $value[0]; 
            $lon = $value[1]; 
                $coordonnees[$i]=array($lat,$lon);
            $i++;

        }

        return $coordonnees;

    }

    
    /////////////////////////////////////////
    //      displayListActivities
    /////////////////////////////////////////

    
    function displayListActivities($id_strava_athlete,$access_token){
        $conn = OpenConnexion();
        
        echo "<B><U>Liste des activités enregistrées :</B></U> ". "<br>";
        $sql = 'SELECT activity_date, activity_name, activity_distance, activity_elevation,activity_sport, id_strava_activity  FROM activity WHERE id_strava_athlete ='. $id_strava_athlete ;
        $result = $conn->query($sql);       

        if ($result->num_rows > 0) {                                       
        #-----------------------------------
        echo '<table style="width:1000px">';
        echo "<tr>";
            //echo "<th>Strava Id</th>";   
            echo "<th>Date</th>";
            echo "<th>Name</th>";
            echo "<th>Distance</th>";
            echo "<th>Elevation</th>";                              
            echo "<th>Sport</th>";                              
        echo"</tr>";
        #-----------------------------------
        // output data of each row
        while($row = $result->fetch_assoc()) {
                $id_strava_activity = $row[id_strava_activity];
                $act_date = $row[activity_date];
                $act_name = $row[activity_name];                            
                $activity_distance = round($row[activity_distance]/1000,2);                                     
                $activity_elevation = $row[activity_elevation];                                  
                $activity_sport = $row[activity_sport];                      
                echo "<tr>";              
                echo "<td>" . $act_date . "</td>";                
                echo "<td><a href='activity.php?id_strava_activity=".$id_strava_activity. "&access_token=".$access_token. "'>" . utf8_encode($act_name) . "</a></td>";
                echo "<td>" . $activity_distance . "</td>";
                echo "<td>" . $activity_elevation . "</td>";
                echo "<td>" . $activity_sport . "</td>";               
                echo "</tr>";
            }                            
        echo "</table>";           

        }   

        $conn->close();  
    }   


    /////////////////////////////////////////
    //      Return liste des cols
    /////////////////////////////////////////

    

    function returnColList (){

        $conn = OpenConnexion();
        
        #$sql = "SELECT col_nom,col_lat,col_lon,col_alt  FROM col where col_nom='Col de Rotisson'";
        $sql = "SELECT col_nom,col_lat,col_lon,col_alt  FROM col";
        $result = $conn->query($sql);       
        $i=0;
        if ($result->num_rows > 0) {                                              
        // output data of each row
            while($row = $result->fetch_assoc()) {               
                
                $col_nom = utf8_encode($row[col_nom]);
                $col_lon = $row[col_lon];
                $col_lat = $row[col_lat];                            
                $col_alt = $row[col_alt];

                $col[$i]=array($col_nom,$col_lon,$col_lat,$col_alt);
                $i++;

            }   
        }        

        $conn->close();  
        return $col;
    }

    

    
?>


