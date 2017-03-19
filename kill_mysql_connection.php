$result = mysql_query("SHOW FULL PROCESSLIST");
while ($row=mysql_fetch_array($result)) {
  $process_id=$row["Id"];
  if ($row["db"] == "iShare_data" ) {
    $sql="KILL $process_id";
    mysql_query($sql);

}

}
