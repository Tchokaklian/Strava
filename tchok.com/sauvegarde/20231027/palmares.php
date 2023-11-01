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
                        
        if (isset($_POST['email'])){        
            $email = stripslashes($_REQUEST['email']);        
        }

        if (isset($_POST['password'])){        
            $password = stripslashes($_REQUEST['password']);        
        }

        if (isset($_POST['period'])){        
            $period = ($_POST['period']);                    
        }

        require_once 'sqldb.php';
                
        getListActivities($email,$password,$period);

        //https://www.strava.com/api/v3/athlete/activities?access_token=23cd5412679a0cd625a8755c2de8269f23085140&perpage=60

    ?>    

</body>
</html>    