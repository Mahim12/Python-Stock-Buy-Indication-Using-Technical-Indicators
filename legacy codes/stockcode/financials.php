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
        }

        .btn-danger:focus {
            background: #f39700;
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
        <div class="row mt-3">
            <div class='col-lg-12 col-md-12 col-12 mb-lg-2 mb-md-2 mb-2'>
                <a class="btn btn-danger" href="https://docs.google.com/spreadsheets/d/1oYEdKCrZ__5gPd4CbKTFXdBMHiQbsu0PmgYy8MJkizg/edit#gid=0" target="_blank">Insert</a>
            </div>
            <div class='col-lg-12 col-md-12 col-12 mb-lg-2 mb-md-2 mb-2'>
                <iframe width="100%" height="450px" src="https://docs.google.com/spreadsheets/d/e/2PACX-1vShaZT6LYP4A7zSnbKU6nUkbrwG1dD5kdBb1GSA3tu6w3Jy9E6RbnJJAg98fA2i2N8jyzup7YIHYYIK/pubhtml?widget=true&amp;headers=false"></iframe>
            </div>
        </div>
    </div>
    <script>
    </script>
</body>

</html>