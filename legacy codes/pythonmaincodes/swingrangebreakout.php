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
        <div class="modal fade" id="rangebreakout" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-xl" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h3 class="modal-title" id="exampleModalLongTitle">Swing Range Breakout Trading Strategy</h3>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <h5>Key things to remember on Swing Range Breakout Trading</h5>
                        <ol>
                            <li>
                                <h6>The prices before the last ten days were in a range.</h6>
                            </li>
                            <li>
                                <h6>The recent ten prices broke out of that range.</h6>
                            </li>
                            <li>
                                <h6>Check if the RSI has been increasing or not.</h6>
                            </li>
                            <li>
                                <h6>Check if the ADX has been increasing or not.</h6>
                            </li>
                        </ol>
                    </div>
                </div>
            </div>
        </div>
        <div class="row mt-5">
            <div class='col-lg-10 col-md-10 col-12'>
                <h5 style="color: white;">Swing Range Breakout Trading</h5>
            </div>
            <div class='col-lg-2 col-md-2 col-12'>
                <button type="button" class="btn btn-danger" data-toggle="modal" data-target="#rangebreakout">
                    Learn More
                </button>
            </div>
        </div>

        <div class="row mt-3">
            <div class='col-lg-12 col-md-12 col-12'>
                <div class="table-content table-responsive" id="rangebreakouttrading">
                    <?php
                    function adxrsirange($filename, $header = false)
                    {
                        $handle = fopen($filename, "r");
                        echo '<table class= "table table-sm table-hover table-striped"><thead class = "thead">';
                        //display header row if true
                        if ($header) {
                            $csvcontents = fgetcsv($handle);
                            echo '<tr>';
                            foreach ($csvcontents as $headercolumn) {
                                echo "<th>$headercolumn</th>";
                            }
                            echo '</tr></thead><tbody id="myswingTable">';
                        }
                        // displaying contents
                        while ($csvcontents = fgetcsv($handle)) {
                            echo '<tr>';
                            foreach ($csvcontents as $column) {
                                echo "<td>$column</td>";
                            }
                            echo '</tr>';
                        }
                        echo '</tbody></table>';
                        fclose($handle);
                    }
                    adxrsirange('strategies/swing trading/trend trading/rangebreakouttrading.csv', true);
                    ?>
                </div>
            </div>
        </div>
    </div>
    <script>
        setInterval(function() {
            $("#rangebreakouttrading").load("swingrangebreakout.php #rangebreakouttrading"); // this will run after every 2 seconds
        }, 2000);
    </script>
</body>

</html>