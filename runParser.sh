#!/bin/bash
python skeleton_parser.py ebay_data/items-*.json

cd dat 

sort RawBelong.dat | uniq > Belong.dat
sort RawItem.dat | uniq > Item.dat
sort RawSell.dat | uniq > Sell.dat
sort RawBid.dat | uniq > Bid.dat
sort RawCategory.dat | uniq > Category.dat
sort RawUser.dat | uniq > User.dat