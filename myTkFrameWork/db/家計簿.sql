CREATE TABLE HouseholdAccountBook( 
    userId text
    , receiptId integer
    , purchaseDate date
    , store text
    , money integer
    , remarks text
    , imcomeExpenditure integer
    , draft integer
    , PRIMARY KEY (userId, receiptId)
); 

CREATE TABLE Log( 
    userId text
    , display text
    , itemName text
    , item text
); 

CREATE TABLE userManager( 
    userId text
    , userPassword text
    , userName text
    , Autho text
    , PRIMARY KEY (userId)
); 

CREATE TABLE codeName( 
    columnName not null
    , code text not null
    , name text not null
    , sortNum integer
    , PRIMARY KEY (code)
);

