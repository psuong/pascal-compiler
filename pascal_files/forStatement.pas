program forStatement;
    var x : integer;
    var y : integer;
begin
    for y := 0 to 10 do
    begin
        writeln(y);
        y := y + 1;
    end;

    for x := 10 downto 0 do
    begin
        writeln(x);
        x := x - 1;
    end;
end.
