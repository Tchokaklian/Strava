<?php     
                    
    if (isset($_POST['email'])){        
        $email = stripslashes($_REQUEST['email']);        
    }

    if (isset($_POST['password'])){        
        $password = stripslashes($_REQUEST['password']);        
    }

    require_once 'sqldb.php';
    
    getListActivities($email,$password);

    //https://www.strava.com/api/v3/athlete/activities?access_token=23cd5412679a0cd625a8755c2de8269f23085140&perpage=60

?>    