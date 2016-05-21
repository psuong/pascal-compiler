program ifStatements;
    var x : integer;
    var y : integer;
    var z : integer;
begin
    x := 5;
    y := 666;
    z := 3;

    if x > y then
        writeln(z);
    else
        writeln(y);

    if z < x then
        writeln(x);
    else
        writeln(z);
end.
