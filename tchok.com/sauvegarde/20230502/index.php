<html>
<head>
       <title>100 Cols</title>       
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

       <hr>
       
       <?php     
              
              include "envvar.php";
              #$dbHost = 'tchokcommcdbo100.mysql.db';
              #$dbBase = 'tchokcommcdbo100';
              #$dbUser = 'tchokcommcdbo100';
              #$dbPassword = 'Sarkis19';

              #echo "<p>Php version :" . phpversion() . "</p>\n";
              #echo "<pre>\n";

              /*** msqli procédural ***/
              $mysqli = mysqli_connect( $dbHost, $dbUser, $dbPassword, $dbBase );
              if ( mysqli_connect_errno( $mysqli ) ) {
	              echo "Échec connexion mysqli_connect : " . mysqli_connect_error() . "<br>\n";
              } else {
                     #echo "Connexion possible avec mysqli_connect (procédural)<br>\n";
                     #echo "<pre>\n";

                     echo "<B><U>Liste des cols routiers des Alpes Maritimes</B></U> ". "<br>";

                     $sql = 'SELECT col_nom, col_alt FROM col' ;
                     $result = $mysqli->query($sql);       

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
                     $mysqli->close();       
              }              
              
       ?>


</body>
</html>