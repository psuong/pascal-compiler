program repeatStatement;
    var x : integer;
begin
    x := 0;

    repeat
        x := x + 10;
        writeln(x);
    until x = 50;
    writeln(x);
end.
