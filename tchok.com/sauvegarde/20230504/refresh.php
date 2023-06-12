<?php     
    
    require_once 'sqldb.php';
            
    if (isset($_POST['email'])){        
        $email = stripslashes($_REQUEST['email']);        
    }

    if (isset($_POST['password'])){        
        $password = stripslashes($_REQUEST['password']);        
    }

    refreshToken($email,$password);

?>    