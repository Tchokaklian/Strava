<html>
<head>       
       <title>100 Cols </title>       
       <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />                                   
</head>
<body>         
       <table>
       <thead>
              <tr>
              <th colspan="2">Connecter Strava au Club des 100 Cols</th>              
              </tr>             
       </thead>
       <tbody>
              <tr>              
                     <td><img src="images/150_club-des-cent-cols.png"></td>
                     <td><img src="images/150_strava1.png"></td>              
              </tr>
       </tbody>
       </table>


       <form action="strava_auth.php" method="get">
              Entrez votre email :     <input type="email" name="mailstrava" />
              <input type="submit" name="submit" />     
       </form>

       <hr>
       
       <form class="box" action="palmares.php" method="post">              
              Voir votre palmarès de cols
                     <input type="text" class="box-input" name="email" placeholder="Email" required />
                     <input type="password" class="box-input" name="password" placeholder="Mot de passe" required />
                     <input type="submit" name="submit" value="Entrer" class="box-button" />              
       </form>
              
       <!--
       <hr>
       <form class="box" action="refresh.php" method="post">              
              Refresh du jeton
                     <input type="text" class="box-input" name="email" placeholder="Email" required />
                     <input type="password" class="box-input" name="password" placeholder="Mot de passe" required />
                     <input type="submit" name="submit" value="Entrer" class="box-button" />              
       </form>
       -->

       <hr>
       
       <?php      
              require_once "sqldb.php";              
              getListeCols();                    
       ?>


</body>
</html>