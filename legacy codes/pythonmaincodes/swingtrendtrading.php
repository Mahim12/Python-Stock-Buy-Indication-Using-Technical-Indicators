<!DOCTYPE html>
<html>

<head>
    <title>Hybrid Tactics</title>
    <link rel="icon" type="image/svg" href="assets/photos/icons/favicon.svg" />
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js"></script>
    <link rel="stylesheet" href="css/style.css" type="text/css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <style>
    </style>
</head>

<body>
    <nav class="navbar navbar-expand-lg sticky-top navbar-light bg-light">
        <a class="navbar-brand" href="Home.php">Hybrid Tactics</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo02" aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarTogglerDemo02">
            <ul class="navbar-nav mr-auto mt-2 mt-lg-0 mr-lg-4">
                <li class="nav-item">
                    <a class="nav-link navs-link" href="Financials.php" href="#">Financials</a>
                </li>
                <li class="nav-item dropdown">
                    <a class="nav-link navs-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        Strategies
                    </a>
                    <div class="dropdown-menu" aria-labelledby="navbarDropdown">
                        <a class="dropdown-item" href="swingtrendtrading.php">Swing Trend Strategy</a>
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item" href="meanreversion.php">Swing Mean Reversion</a>
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item" href="intraday.php">Intraday Trading</a>
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item" href="midtouch.php">Midtouch Trading</a>
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item" href="schaffbuy.php">SchaffBuy Trading</a>
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item" href="swingrangebreakout.php">Swing Range Breakout Trading</a>
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item" href="bandopencrossover.php">Price MidBand Crossover Trading</a>
                        <div class="dropdown-divider"></div>
                    </div>
                </li>
            </ul>
            <form class="form-inline my-2 my-lg-0" method="post" name="name" action="Search.php" target="_self">
                <input class="form-control mr-sm-2" name="name" type="search" placeholder="I want to compare. . ." required>
                <button class="btn btn-danger my-2 my-sm-0" type="submit" onsubmit="return OnButton1();">Search</button>
            </form>
        </div>
    </nav>
    <div class="container mt-5 mt-lg-3">
        <div class="row">
            <div class='col-lg-12 col-md-12 col-12'>
                <div class="objective-container">
                    <h3> Objective: 5000 bucks from 17th Nov to 17th Dec.</h3>
                </div>
            </div>
        </div>

        <!-- Modal -->
        <div class="modal fade" id="slopetrend" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-xl" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h3 class="modal-title" id="exampleModalLongTitle">Slope Trend Trading</h3>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <h5>Key things to remember on trend trading.</h5>
                        <ol>
                            <li>
                                <h6>Slope and the angle are steeper of the price</h6>
                            </li>
                            <li>In a strong uptrend, the prices usually fluctuate between the upper band and the middle band (The moving average) of the bollinger bands. When that happens, a crossing below the 20-day moving average warns of a trend reversal to the downside. </li>
                            <li>In a strong downtrend, the prices usually fluctuate between the lower band and the middle band (The moving average) of the bollinger bands. When that happens, a crossing above the 20-day moving average warns of a trend reversal to the upside. </li>
                            <li>RSI is usually moving up in the graph, check it. Once it reaches around 80(give or take a few), it falls a little along with the price but not below 50.</li>
                            <li><a href="https://www.investopedia.com/articles/trading/07/adx-trend-indicator.asp">ADX</a></li>
                            <li>ADX is non-directional; it registers trend strength whether price is trending up or down./li>
                            <li>choppiness</li>
                            <li>Price channel represented using support and resistance.</li>
                            <li>For reversal: When stock prices continually touch the upper Bollinger Band®, the prices are thought to be overbought; conversely, when they continually touch the lower band, prices are thought to be oversold, triggering a buy signal.</li>
                            <li>For reversal: When price moved higher from one peak to another but ADX moved to lower from one peak to another as shown in the link of adx. It is a sign of divergence or a reversal.</li>
                            <li>
                                <p>The Squeeze
                                    <br>
                                    The squeeze is the central concept of Bollinger Bands®. When the bands come close together, constricting the moving average, it is called a squeeze. A squeeze signals a period of low volatility and is considered by traders to be a potential sign of future increased volatility and possible trading opportunities. Conversely, the wider apart the bands move, the more likely the chance of a decrease in volatility and the greater the possibility of exiting a trade. However, these conditions are not trading signals. The bands give no indication when the change may take place or which direction price could move.
                                    <br>
                                    Breakouts
                                    <br>
                                    Approximately 90% of price action occurs between the two bands. Any breakout above or below the bands is a major event. The breakout is not a trading signal. The mistake most people make is believing that that price hitting or exceeding one of the bands is a signal to buy or sell. Breakouts provide no clue as to the direction and extent of future price movement.</p>
                            </li>
                        </ol>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-5">
            <div class='col-lg-10 col-md-10 col-12'>
                <h2 style="color: white;">SLOPE TREND TRADING</h2>
            </div>
            <div class='col-lg-2 col-md-2 col-12'>
                <button type="button" class="btn btn-danger" data-toggle="modal" data-target="#slopetrend">
                    Learn More
                </button>
            </div>
        </div>

        <div class="row">
            <div class='col-lg-12 col-md-12 col-12'>
                <div class="table-content table-responsive" id="swingtrend">
                    <?php
                    $servername = "localhost";
                    $username = "root";
                    $password = "";
                    $dbname = "hybridtactics";

                    // Create connection
                    $conn = new mysqli($servername, $username, $password, $dbname);
                    // Check connection
                    if ($conn->connect_error) {
                        die("Connection failed: " . $conn->connect_error);
                    }
                    echo '<table class= "table table-sm table-hover table-striped"><thead class = "thead"><tr><th class="table-element">INDEX</th><th>COMPANY</th><th class="table-element">SLOPE</th><th class="table-element">ANGLE</th><th>PERCENTILE</th><th>PRICE</th><th>EMA</th><th class="table-element">RSI</th><th class="table-element">ADX</th></tr></thead><tbody id="myswingTable">';
                    $sql = "SELECT * FROM `swingtrend`";

                    $result = $conn->query($sql);

                    if ($result->num_rows > 0) {
                        // output data of each row
                        while ($row = $result->fetch_assoc()) {
                            echo "<tr><td class='table-element'>" .  $row["index"] . "</td><td><a href='#" .  $row["Company"] . "'>" .  $row["Company"] . "</a></td><td  class='table-element'> " .  $row["Slope"] . "</td><td  class='table-element'> " .  $row["Angle"] . "</td><td> " .  $row["CPP"] . "</td><td> " .  $row["Price"] . "</td><td> " .  $row["EMA Value"] . "</td><td  class='table-element'> " .  $row["RSI"] . "</td><td  class='table-element'> " .  $row["ADX"] . "</td></tr>";
                        }
                    } else {
                        echo "0 results";
                    }
                    echo '</tbody></table>';

                    $conn->close();
                    ?>
                </div>
            </div>
        </div>
        <div class="row">
            <?php
            $images = array();
            $directory = 'slope images';
            $files = scandir($directory);
            shuffle($files);
            if ($handle = opendir($directory)) {
                while (false !== ($file = readdir($handle))) {
                    if (preg_match("/\.png$/", $file)) $images[] = $file;
                    elseif (preg_match("/\.jpg$/", $file)) $images[] = $file;
                    elseif (preg_match("/\.jpeg$/", $file)) $images[] = $file;
                    elseif (preg_match("/\.gif$/", $file)) $images[] = $file;
                }

                shuffle($images);
                closedir($handle);
            }
            ?>
            <?php
            foreach ($files as $item) {
                if ($item != '.' && $item != '..') {
                    $path = $directory . '/' . $item;
                    $x = substr($item, 0, strrpos($item, '.'));
                    echo '<div class="col-lg-12 col-md-12 col-12 mt-2"><div class = "slope-tactics-image-container" id = "' . $x . '"> <img style="width:100%; height:100%; object-fit:contain;" src="' . $path . '"/> </div></div>';
                }
            }
            ?>
        </div>
    </div>
    <script>
    </script>
</body>

</html>