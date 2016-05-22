program forStatement;
    var x : integer;
    var y : integer;
begin
    x := 0;

    for y := 10 to 0 do
    begin
        writeln(y);
        y := y - 1;
    end;
end.
