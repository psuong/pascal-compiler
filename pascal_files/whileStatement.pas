program whileStatement;
    var x : integer;
    var y : integer;
    var z : integer;
begin
    x := 0;
    y := 5;
    z := 20;

    while x < 10 do
        begin
            x := x + 1;
            writeln(x);
        end;
    writeln(x);
end.
