<?php     
    
    include "envvar.php";            
            
    if (isset($_POST['email'])){        
        $email = stripslashes($_REQUEST['email']);        
    }

    if (isset($_POST['password'])){        
        $password = stripslashes($_REQUEST['password']);        
    }

    $mysqli = mysqli_connect( $dbHost, $dbUser, $dbPassword, $dbBase );
    if ( mysqli_connect_errno( $mysqli ) ) {
        echo "Échec connexion mysqli_connect : " . mysqli_connect_error() . "<br>\n";
    } else {

        $sql = "SELECT first_name, last_name, access_token, refresh_token, athlete_id, client_code FROM strava_user ";
        $sql = $sql. "WHERE email = '" . $email . "' AND password = '" . $password . "'";

        #echo $sql ;

        $result = $mysqli->query($sql);

        if ($result->num_rows > 0) {
           
            while($row = $result->fetch_assoc()) {
                $first_name = $row["first_name"];
                $last_name = $row["last_name"];
                $access_token = $row["access_token"];
                $refresh_token = $row["refresh_token"];
                $athlete_id = $row["athlete_id"];
                $client_code = $row["client_code"];

                //echo $last_name . " " . $first_name . " ... Connexion réussie ! ";

                // "https://www.strava.com/api/v3/athlete/activities?before=&after=&page=&per_page=" "Authorization: Bearer [[token]]"        

                //$url = "https://www.strava.com/api/v3/athlete/activities?before=&after=&page=&per_page=" "Authorization: Bearer [[token]]"        
                //$curl = curl_init($url);

                //curl_setopt($curl, CURLOPT_POST, true);
                //curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
                //$result = curl_exec($curl);
    
                //curl_close($curl);

                ##########################
                //print $result;
                ##########################

                //$jsonArrayResponse = json_decode($result);





              }
            
        } else {
            echo "Erreur , email ou mot de passe invalide !";
        }

        $mysqli->close(); 

    }







?>    