<?php

    //include "envvar.php";
    include "sqldb.php";

    $dbHost = 'tchokcommcdbo100.mysql.db';
    $dbBase = 'tchokcommcdbo100';
    $dbUser = 'tchokcommcdbo100';
    $dbPassword = 'Sarkis19';

    $strava_email = $_GET['state']; // Je squate ce champ ...
    $codeClient = $_GET['code'];    
    
    #echo 'email = '.$strava_email.'<br />'; 
    #echo 'code = '.$codeClient.'<br />'; 
        
    $url = 'https://www.strava.com/api/v3/oauth/token';
    $curl = curl_init($url);

    curl_setopt($curl, CURLOPT_POST, true);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);

    # 2711 = Mon application
    $data = "client_id=2711&client_secret=144e2d05e4b1b91f095dbafe6b40fbc4a9d0933e&code=".$codeClient."&grant_type=authorization_code";
    
    curl_setopt($curl, CURLOPT_POSTFIELDS, $data);

    $result = curl_exec($curl);

    
    curl_close($curl);

    

    ##########################
    #   print $result;
    ##########################
    

    $jsonArrayResponse = json_decode($result);

    
    
    $token_type = '"'. $jsonArrayResponse-> token_type . '"';      
    $access_token = '"'. $jsonArrayResponse-> access_token . '"';
    $expires_at = '"'. $jsonArrayResponse-> expires_at . '"';
    $refresh_token = '"'. $jsonArrayResponse-> refresh_token . '"';
    $access_token = '"'. $jsonArrayResponse-> access_token . '"';
    $athlete_id = $jsonArrayResponse-> athlete -> id;
    $first_name = '"'. $jsonArrayResponse-> athlete -> firstname . '"';
    $last_name = '"'. $jsonArrayResponse-> athlete -> lastname . '"';
    $city = '"'. $jsonArrayResponse-> athlete -> city . '"';
    $country = '"'. $jsonArrayResponse-> athlete -> country . '"';
    $sex = '"'. $jsonArrayResponse-> athlete -> sex . '"';
    $strava_email = '"'. $strava_email . '"';
    $codeClient = '"'. $codeClient . '"';
    
    
    addStravaUser($token_type,$access_token,$expires_at,$refresh_token,$athlete_id,$first_name,$last_name,$city,$country,$sex,$strava_email,$codeClient);

?>

