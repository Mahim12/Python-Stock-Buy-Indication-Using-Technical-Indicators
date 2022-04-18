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
        .btn-danger {
            background: #febd69;
            border: #febd69;
        }

        .btn-danger:hover {
            background: #f39700;
            border: #f39700;
        }

        .btn-danger:focus {
            background: #f39700;
            border: #f39700;
        }


        .slope-tactics-image-container {
            height: 450px;
            border: 1px solid rgba(0, 0, 0, .125);
        }

        .intraday-strategy-label {
            color: black;
            font-size: 28px;
            FONT-WEIGHT: 640;
        }

        .table-header-contents {
            margin-top: 50px;
            padding: 0px 30px;
        }

        .thead {
            background-color: #35708a !important;
            color: white;
        }

        .table-content {
            padding: 0px 0px;
        }

        table {
            table-layout: fixed;
            width: 100%;

        }

        .table-element {
            overflow: hidden;
            width: 5.3em;
            white-space: nowrap;
            text-overflow: ellipsis;
        }

        .dropdown-item {
            background-color: transparent;
            color: black;
        }


        .dropdown-item:hover {
            background-color: #febd69;
            color: white;
        }

        .dropdown-menu {
            padding: 0px;
            color: white;
        }


        .table-hover tbody tr:hover {
            color: #343a40;
            background-color: #febd69;
        }

        .objective-container {
            text-align: center;
            border: 1px solid rgba(0, 0, 0, .125);
            padding: 30px;
            color: #febd69;
        }

        tr {
            line-height: 30px;
            min-height: 30px;
            height: 30px;
            border-bottom: 1px solid rgba(0, 0, 0, .125);
        }
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
                        <a class="dropdown-item" href="meanreversion.php">Mean Reversion</a>
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
    <div class="page-footer hide-on-desktop-only">
        <div class="search-container">
            <form method="post" name="name" action="Search.php" target="_self">
                <input type="search" placeholder="I want to compare. . ." name="name" required>
                <button onsubmit="return OnButton1();" type="submit"><i class="fa fa-search"></i></button>
            </form>
        </div>
    </div>
    <div class="container mt-5 mt-lg-3">
        <div class="row">
            <div class='col-lg-12 col-md-12 col-12'>
                <div class="objective-container">
                    <h3 style="color: #dc3545;"> Objective: 5000 bucks from 17th Nov to 17th Dec.</h3>
                </div>
            </div>
        </div>
        <div class="modal fade" id="bollingermidcrossover" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-xl" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h3 class="modal-title" id="exampleModalLongTitle">Bollinger Mid-CrossOver Strategy</h3>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <h5>Key things to remember on Bollinger Mid cross over trading.</h5>
                        <ol>
                            <li>
                                <h6>Current Price> Middle band values</h6>
                            </li>

                        </ol>
                    </div>
                </div>
            </div>
        </div>
        <div class="modal fade" id="adxrsirange" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-xl" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h3 class="modal-title" id="exampleModalLongTitle">Adx-Rsi Range Trading Strategy</h3>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <h5>Key things to remember on Adx-Rsi Range Trading</h5>
                        <ol>
                            <li>
                                <h6>Range selected based on RSI AND ADX</h6>
                            </li>
                        </ol>
                    </div>
                </div>
            </div>
        </div>
        <div class="modal fade" id="bollingerrange" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-xl" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h3 class="modal-title" id="exampleModalLongTitle">Bollinger-Range Strategy</h3>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <h5>Key things to remember on Bollinger Range Trading</h5>
                        <ol>
                            <li>
                                <h6>Range selected based on Bollinger Band Values</h6>
                            </li>
                        </ol>
                    </div>
                </div>
            </div>
        </div>
        <div class="modal fade" id="slope0" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-xl" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h3 class="modal-title" id="exampleModalLongTitle">Slope = 0 Strategy</h3>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <h5>Key things to remember on Slope = 0 Trading</h5>
                        <ol>
                            <li>
                                <h6>Slope of the trend line is 0 to indicate range</h6>
                            </li>
                        </ol>
                    </div>
                </div>
            </div>
        </div>
        <div class="row mt-5">
            <div class='col-lg-10 col-md-10 col-12'>
                <h5>Bollinger Mid-CrossOver Strategy</h5>
            </div>
            <div class='col-lg-2 col-md-2 col-12'>
                <button type="button" class="btn btn-danger" data-toggle="modal" data-target="#bollingermidcrossover">
                    Learn More
                </button>
            </div>
        </div>
        <div class="row mt-3">
            <div class='col-lg-12 col-md-12 col-12'>
                <div class="table-content">
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
                    echo '<table class= "table table-sm table-hover table-striped"><thead class = "thead"><tr><th>COMPANY</th><th>SQUEEZE VALUE</th><th>PERCENTILE</th><th>PRICE</th></tr></thead><tbody id="myswingTable">';
                    $sql = "SELECT *  FROM `bollingermidcrossover`";

                    $result = $conn->query($sql);

                    if ($result->num_rows > 0) {
                        // output data of each row
                        while ($row = $result->fetch_assoc()) {
                            echo "<tr><td>" .  $row["company"] . "</td><td> " .  $row["bollingersquueze"] . "</td><td> " .  $row["cpp"] . "</td><td> " .  $row["price"] . "</td></tr>";
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

        <div class="row mt-5">
            <div class='col-lg-10 col-md-10 col-12'>
                <h5>Adx-Rsi Range Trading</h5>
            </div>
            <div class='col-lg-2 col-md-2 col-12'>
                <button type="button" class="btn btn-danger" data-toggle="modal" data-target="#adxrsirange">
                    Learn More
                </button>
            </div>
        </div>

        <div class="row mt-3">
            <div class='col-lg-12 col-md-12 col-12'>
                <div class="table-content">
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
                    echo '<table class= "table table-sm table-hover table-striped"><thead class = "thead"><tr><th>COMPANY</th><th>PERCENTILE</th><th>PRICE</th><th>RSI</th><th>ADX</th><th>EMA</th></tr></thead><tbody id="myswingTable">';
                    $sql = "SELECT *  FROM `rtrade`";

                    $result = $conn->query($sql);

                    if ($result->num_rows > 0) {
                        // output data of each row
                        while ($row = $result->fetch_assoc()) {
                            echo "<tr><td>" .  $row["company"] . "</td><td> " .  $row["cpp"] . "</td><td> " .  $row["price"] . "</td><td> " .  $row["rsi"] . "</td><td> " .  $row["adx"] . "</td><td> " .  $row["ema"] . "</td></tr>";
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

        <div class="row mt-5">
            <div class='col-lg-10 col-md-10 col-12'>
                <h5>Bollinger-Range Trading</h5>
            </div>
            <div class='col-lg-2 col-md-2 col-12'>
                <button type="button" class="btn btn-danger" data-toggle="modal" data-target="#bollingerrange">
                    Learn More
                </button>
            </div>
        </div>
        <div class="row mt-3">
            <div class='col-lg-12 col-md-12 col-12'>
                <div class="table-content">
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
                    echo '<table class= "table table-sm table-hover table-striped"><thead class = "thead"><tr><th>COMPANY</th><th>SQUEEZE VALUE</th><th>PERCENTILE</th><th>PRICE</th></tr></thead><tbody id="myswingTable">';
                    $sql = "SELECT *  FROM `bollingerrange`";

                    $result = $conn->query($sql);

                    if ($result->num_rows > 0) {
                        // output data of each row
                        while ($row = $result->fetch_assoc()) {
                            echo "<tr><td>" .  $row["company"] . "</td><td> " .  $row["bollingersquueze"] . "</td><td> " .  $row["cpp"] . "</td><td> " .  $row["price"] . "</td></tr>";
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
        <div class="row mt-5">
            <div class='col-lg-10 col-md-10 col-12'>
                <h5>Slope = 0 Range Trading</h5>
            </div>
            <div class='col-lg-2 col-md-2 col-12'>
                <button type="button" class="btn btn-danger" data-toggle="modal" data-target="#slope0">
                    Learn More
                </button>
            </div>
        </div>

        <div class="row mt-3">
            <div class='col-lg-12 col-md-12 col-12'>
                <div class="table-content">
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
                    echo '<table class= "table table-sm table-hover table-striped"><thead class = "thead"><tr><th>INDEX</th><th>COMPANY</th><th>SLOPE</th><th>ANGLE</th><th>PERCENTILE</th><th>PRICE</th><th>EMA</th><th>RSI</th><th>ADX</th></tr></thead><tbody id="myswingTable">';
                    $sql = "SELECT *  FROM `sloperangestrategy`";

                    $result = $conn->query($sql);

                    if ($result->num_rows > 0) {
                        // output data of each row
                        while ($row = $result->fetch_assoc()) {
                            echo "<tr><td>" .  $row["index"] . "</td><td>" .  $row["Company"] . "</td><td> " .  $row["Slope"] . "</td><td> " .  $row["Angle"] . "</td><td>" .  $row["CPP"] . "</td><td>" .  $row["Price"] . "</td><td> " .  $row["EMA Value"] . "</td><td> " .  $row["RSI"] . "</td><td> " .  $row["ADX"] . "</td></tr>";
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
    </div>
</body>

</html>