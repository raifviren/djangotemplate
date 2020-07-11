#!/bin/bash

threshold=70

function check_cov {
  pct=`coverage report | tail -n 1 | awk '{print $6}' | sed 's/%$//g'`
  if [ $pct -ge $threshold ]
  then
    echo "PASS: $pct% Code coverage is greater than required threshold: $threshold%"
    return 0
  else
    echo "ERROR: $pct% Code coverage is below required threshold: $threshold% !!!"
    return 1
  fi
}

check_cov
