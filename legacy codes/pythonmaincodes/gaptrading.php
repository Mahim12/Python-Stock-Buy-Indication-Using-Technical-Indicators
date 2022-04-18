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
                        <a class="dropdown-item" href="gaptrading.php">Gap Trading</a>
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
        <div class="row">
            <div class="col-lg-12 col-md-12 col-12">
                <div id="demo" class="carousel slide" data-ride="carousel">
                    <!-- The slideshow -->
                    <div class="carousel-inner">
                        <div class="carousel-item active">
                            <div class="row">

                                <?php
                                $images = array();
                                $directory = 'assets/photos/first six';
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
                                        echo '<div class="col-lg-2 col-md-2 col-12"><div class="row"><div class="col-lg-12 col-md-12 col-12"><div class="roller-images"><img src="' . $path . '" alt="image" style="width:100%; height:100%; object-fit:contain;"/></div></div></div></div>';
                                    }
                                }
                                ?>

                            </div>
                        </div>
                        <div class="carousel-item">
                            <div class="row">

                                <?php
                                $images = array();
                                $directory = 'assets/photos/second six';
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
                                        echo '<div class="col-lg-2 col-md-2 col-12"><div class="row"><div class="col-lg-12 col-md-12 col-12"><div class="roller-images"><img src="' . $path . '" alt="image" style="width:100%; height:100%; object-fit:contain;"/></div></div></div></div>';
                                    }
                                }
                                ?>

                            </div>
                        </div>
                        <div class="carousel-item">
                            <div class="row">

                                <?php
                                $images = array();
                                $directory = 'assets/photos/third six';
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
                                        echo '<div class="col-lg-2 col-md-2 col-12"><div class="row"><div class="col-lg-12 col-md-12 col-12"><div class="roller-images"><img src="' . $path . '" alt="image" style="width:100%; height:100%; object-fit:contain;"/></div></div></div></div>';
                                    }
                                }
                                ?>

                            </div>
                        </div>
                    </div>
                    <!-- Left and right controls -->
                    <a class="carousel-control-prev" href="#demo" data-slide="prev"> <span class="carousel-control-prev-icon"></span> </a>
                    <a class="carousel-control-next" href="#demo" data-slide="next"> <span class="carousel-control-next-icon"></span> </a>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="modal fade" id="gaptrade" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered modal-xl" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h3 class="modal-title" id="exampleModalLongTitle">Gap Trade Strategy</h3>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">
                            <h5>Key things to remember on Gap Trading</h5>
                            <ol>
                                <li>
                                    <h6>Trade an actual GAP.</h6>
                                </li>
                                <li>
                                    <h6>If gaps are greater than 1.9 then better.</h6>
                                </li>
                                <li>
                                    <h6>Check candle of previous day. Hope it's not too sharp.</h6>
                                </li>
                                <h6>For Down Gap Strategy</h6>
                                </li>
                                <li>Maybe Buy almost immediately</li>
                                <li>Study about scalping vs holding the gap stocks. Analyze more.</li>
                                <li>Seems like it increases upto mid-day.</li>
                                <li>
                                    <h6>For Up Gap Strategy</h6>
                                </li>
                                <li>For those that gapped up, it would be better to wait and buy after the price crosses the middle bollinger band.</li>
                                <li>It seems as though if the prices are too sharp, there is a chance of reversal. Learn more from machine learning.</li>
                                <li>
                                    <h6>Check support and resistance with the previous day close.</h6>
                                </li>
                            </ol>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-lg-12 col-md-12 col-12">
                <div class="row">
                    <div class="col-lg-6 col-md-6 col-12">
                        <div class="row mt-5">
                            <div class='col-lg-12 col-md-12 col-12'>
                                <h3 style="color: white;">Down Gap Strategy</h3>
                            </div>
                        </div>

                        <div class="row">
                            <div class='col-lg-12 col-md-12 col-12'>
                                <div class="table-content table-responsive" id="downgaptrading">
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
                                    echo '<table class= "table table-sm table-hover table-striped"><thead class = "thead"><tr><th>COMPANY</th><th>GAP</th></tr></thead><tbody id="myswingTable">';
                                    $sql = "SELECT Company,Gap  FROM `downgaptrading`";

                                    $result = $conn->query($sql);

                                    if ($result->num_rows > 0) {
                                        // output data of each row
                                        while ($row = $result->fetch_assoc()) {
                                            echo "<tr><td style = 'font-weight:500;'>" .  $row["Company"] . "</td><td> " .  $row["Gap"] . "</td></tr>";
                                        }
                                    } else {
                                    }
                                    echo '</tbody></table>';

                                    $conn->close();
                                    ?>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-6 col-md-6 col-12">
                        <div class="row mt-5">
                            <div class='col-lg-12 col-md-12 col-12'>
                                <h3 style="color: white;">Up Gap Strategy</h3>
                            </div>
                        </div>

                        <div class="row">
                            <div class='col-lg-12 col-md-12 col-12'>
                                <div class="table-content table-responsive" id="upgaptrading">
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
                                    echo '<table class= "table table-sm table-hover table-striped"><thead class = "thead"><tr><th>COMPANY</th><th>GAP</th></tr></thead><tbody id="myswingTable">';
                                    $sql = "SELECT Company,Gap  FROM `upgaptrading`";

                                    $result = $conn->query($sql);

                                    if ($result->num_rows > 0) {
                                        // output data of each row
                                        while ($row = $result->fetch_assoc()) {
                                            echo "<tr><td style = 'font-weight:500;'>" .  $row["Company"] . "</td><td> " .  $row["Gap"] . "</td></tr>";
                                        }
                                    } else {
                                    }
                                    echo '</tbody></table>';

                                    $conn->close();
                                    ?>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row mt-5 mb-5">
                    <div class='col-lg-12 col-md-12 col-12'>
                        <div class="objective-container">
                            <div class="row mt-5">
                                <div class='col-lg-8 col-md-6 col-12' style="text-align: left;">
                                    <h2>Gap Trading Strategy</h2>
                                </div>
                                <div class='col-lg-3 col-md-6 col-12' style="text-align: left;">
                                    <button type="button" class="btn btn-danger" data-toggle="modal" data-target="#gaptrade">
                                        Learn More
                                    </button>
                                </div>
                            </div>
                            <div class="row mt-5">
                                <div class='col-lg-6 col-md-4 col-12' style="text-align: left;">
                                    <h6>List of stocks not allowed for intraday trading</h6>
                                </div>
                                <div class='col-lg-2 col-md-2 col-12' style="text-align: right; color:#343a40;">
                                    <a href="https://support.zerodha.com/category/trading-and-markets/margin-leverage-and-product-and-order-types/articles/list-of-scrips-mis-bo-co-gsm-asm">Learn More</a>
                                </div>
                                <div class='col-lg-4 col-md-2 col-12' style="text-align: left; color:#343a40;">
                                    <a href="https://www1.nseindia.com/products/content/derivatives/equities/sec_ban.htm">Security in Ban Period</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>



            </div>
        </div>
        <script>
            setInterval(function() {
                $("#upgaptrading").load("home.php #upgaptrading"); // this will run after every 2 seconds
            }, 2000);
            setInterval(function() {
                $("#downgaptrading").load("home.php #downgaptrading"); // this will run after every 2 seconds
            }, 2000);
        </script>
</body>

</html>