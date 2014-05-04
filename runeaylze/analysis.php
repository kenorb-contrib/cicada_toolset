<?php
	$data = "";
	if(isset($_GET['data']) && file_exists(dirname(__FILE__)."/".$_GET['data'].".cryp_analyze")) {
		$data = explode("!!",file_get_contents(dirname(__FILE__)."/".$_GET['data'].".cryp_analyze"));
	} else 
		$data = explode("!!",file_get_contents("data.cryp_analyze"));
	$rune_num = $data[0];
	$ioc = $data[1];
	$friedman = $data[2];
	$kasiski = $data[3];
	$distribution_count = explode(",",$data[4]);
	$distribution_perc = explode(",",$data[5]);
	$text = $data[6];
	
	$distribution = "";
	
	// Draw diagram
	$distribution .= "<tr>";
	foreach($distribution_count as $dc){
		$distribution .= "<td style='vertical-align:bottom;'><div style='width:35px;height:".($dc/$rune_num*1000)."px;background-color:green;'></div></td>";
	}
	$distribution .= "</tr><tr class='percentage'>";
	foreach($distribution_perc as $dp) {
		$distribution .= "<td>".$dp."</td>";
	}
	$distribution .= "</tr>";
?>
<!DOCTYPE HTML>
<html>
	<head>
		<title>Cicada 3301 Cryptoanalysis</title>
		<style type='text/css'>
			body {
				font-family:Arial,Dejavu Sans Condensed;
			}
			table tr {
				font-size:20px;
				text-align:center;
			}
			.content {
				font-size:20px;
				text-align:justify;
			}
			.leftcolumn {
				text-align:right;
				color:red;
			}
			.rightcolumn {
				text-align:left;
			}
			.percentage {
				font-size:12px;
			}
		</style>
	</head>
	<body>
		<h1>Rune distribution</h1>
		<table>
			<?php echo $distribution; ?>
			<tr>
				<td>&#x16A0;</td>
				<td>&#x16A2;</td>
				<td>&#x16A6;</td>
				<td>&#x16A9;</td>
				<td>&#x16B1;</td>
				<td>&#x16B3;</td>
				<td>&#x16B7;</td>
				<td>&#x16B9;</td>
				<td>&#x16BB;</td>
				<td>&#x16BE;</td>
				<td>&#x16C1;</td>
				<td>&#x16C2;</td>
				<td>&#x16C7;</td>
				<td>&#x16C8;</td>
				<td>&#x16C9;</td>
				<td>&#x16CB;</td>
				<td>&#x16CF;</td>
				<td>&#x16D2;</td>
				<td>&#x16D6;</td>
				<td>&#x16D7;</td>
				<td>&#x16DA;</td>
				<td>&#x16DD;</td>
				<td>&#x16DF;</td>
				<td>&#x16DE;</td>
				<td>&#x16AA;</td>
				<td>&#x16AB;</td>
				<td>&#x16A3;</td>
				<td>&#x16E1;</td>
				<td>&#x16E0;</td>
			</tr>
		</table>
		<h1>Analytic information</h1>
		<table>
			<tr><td class='leftcolumn'>Length:</td><td class='rightcolumn'><?php echo $rune_num; ?></td></tr>
			<tr><td class='leftcolumn'>IOC:</td><td class='rightcolumn'><?php echo $ioc; ?></td></tr>
			<!--<tr><td class='leftcolumn'>Friedman-Keylength:</td><td class='rightcolumn'><?php echo $friedman; ?></td></tr>-->
			<!--<tr><td class='leftcolumn'>Kasiski-Keylengths:</td><td class='rightcolumn'><?php echo $kasiski; ?></td></tr>-->
		</table>
		<h1>Text</h1>
		<div class='content'>
			<?php echo $text; ?>
		</div>
	</body>
</html>
