program arrays;
    var a: array[0..10] of integer;
    var x: integer;
    var i: integer;
begin
    x := 10;

    for i:= 0 to 10 do
        begin
            a[i] := x * 1;
        end;
end.