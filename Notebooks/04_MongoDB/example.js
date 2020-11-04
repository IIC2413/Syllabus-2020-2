var cursor = db.usuarios.find({}, {});
cursor.forEach(
  (element) => {
    try {
      var follows = element["follows"];
      print("## User ID: " + element["uid"]);
      for (var followed in follows) {
        var user_cursor = db.usuarios.find({"uid": follows[followed]},{});
        user_cursor.forEach(
          (user_element) => {
            print(user_element["name"]);
          }
        )
      }
      print("##");
    }
    catch(e) {
      print("GG", e);
    }
  }
);
