
<?php
    
if ( isset( $_GET['submit'] ) ) {
     /* récupérer les données du formulaire en utilisant 
        la valeur des attributs name comme clé 
       */
     $strava_email = $_GET['mailstrava']; 
     
     // afficher le résultat          
     header('Location: https://www.strava.com/oauth/authorize?client_id=2711&response_type=code&redirect_uri=http://www.tchok.com/redirect.php/&approval_prompt=force&scope=read_all,profile:read_all,activity:read_all&state='.$strava_email); 
     exit;
  }

  ?>