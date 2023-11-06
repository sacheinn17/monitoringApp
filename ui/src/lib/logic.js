export function sortByKeyDesc(array, key) {
    return array.sort(function(a, b) {
      var x = a[key];
      var y = b[key];
      return ((x > y) ? -1 : ((x < y) ? 1 : 0));
    });
  }

export async function getTop5Apps(db,day){
    const value = await(db.getAppUsage(day));
    return sortByKeyDesc(value,"time").slice(0,5);
}