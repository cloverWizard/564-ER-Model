DROP TABLE IF EXISTS Item;
CREATE TABLE Item (
    ItemId varchar(100) NOT NULL,
    Name varchar(100),
    Description TEXT,
    Currently REAL,
    Buy_Price REAL,
    First_Bid REAL,
    Number_of_Bids INTEGER,
    PRIMARY KEY (ItemId)
);

DROP TABLE IF EXISTS User;
CREATE TABLE User (
    UserID varchar(100),
    Location varchar(100),
    Country varchar(100),
    Rating REAL, 
    PRIMARY KEY (UserID)
);

DROP TABLE IF EXISTS Category;
CREATE TABLE Category (
    CategoryName varchar(100) NOT NULL,
    PRIMARY KEY (CategoryName)
);

DROP TABLE IF EXISTS Belong;
CREATE TABLE Belong (
    ItemID varchar(100) NOT NULL,
    CategoryName varchar(100) Not NULL,
    PRIMARY KEY (ItemID, CategoryName)
);

DROP TABLE IF EXISTS Sell;
CREATE TABLE Sell (
    ItemID varchar(100),
    UserID varchar(100),
    Started INTEGER,
    Ends INTEGER,
    PRIMARY KEY (ItemID, UserID),
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (ItemID) REFERENCES Item(ItemID)
);

DROP TABLE IF EXISTS Bid;
CREATE TABLE Bid (
    ItemID varchar(100),
    UserID varchar(100),
    BidTime Integer,
    Amount REAL,
    PRIMARY KEY (ItemID, UserID, BidTime),
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (ItemID) REFERENCES Item(ItemID)
);



