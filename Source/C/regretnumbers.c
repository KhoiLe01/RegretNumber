#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include <time.h>

//Testing Khoi

typedef struct {
  float *arr;
  int size;
} Array;

typedef struct {
  float **arr;
  int size;
  int row;
  int col;
} Array2d;

typedef struct {
  float ***arr;
  int size;
  int i;
  int j;
  int k;
} Array3d;

typedef struct {
  float largest_min_regret;
  Array2d *worst_points;
} lower_bound_ret;

//Function Declarations
void arrayInit(Array *a, size_t initialSize);
void arrayAppend(Array *a, float element);
void freeArray(Array *a);
void array2dInit(Array2d *a, int row, int col);
void array2dAppend(Array2d *a, float element);
void freeArray2d(Array2d *a);
void array3dInit(Array3d *a, int i, int j, int k);
void array3dAppend(Array3d *a, float element);
void freeArray3d(Array3d *a);
void lower_upper(int k, int d);
float dot(Array *v1, Array *v2);
float regret(Array *p, Array *points, int utility_repeats);
float set_regret(Array2d *all_points, Array2d *subset, int utility_repeats);
//float smallest_set_regret(vector<vector<float>> all_points, int k, int utility_repeats);
void combinationUtil(Array2d *arr, Array3d *data, Array3d *ret, int start, int end, int index, int r);
Array2d* rescaled(Array2d *points);
lower_bound_ret* lower_bound_random_search(int k, int d, int n, int repeats, int utility_repeats);
//bool dominates (vector<float> x, vector<float> y);
//bool has_dominances(vector<vector<float>> set);
//int choose (int n, int k);
//bool one_in_each_dim (vector<vector<float>> set);
//Struct lower_bound_random_search(int k, int d, int n, int = 1000, int = 100);
//void makeCombi(vector<vector<float>> v1, vector<float> v2, int start, int end, int index, int r);

void arrayInit(Array *a, size_t initialSize)
{
  a->arr = (float *)malloc(initialSize * sizeof(float));
  a->size = 0;
}

void arrayAppend(Array *a, float element)
{
  a->arr[a->size++] = element;
}

void freeArray(Array *a)
{
  free(a->arr);
  a->arr = NULL;
  a->size = 0;
}

void array2dInit(Array2d *a, int row, int col)
{
  a->arr = (float **) malloc(row * sizeof(float *));
  for (int i = 0; i < row; i++)
    a->arr[i] = (float *) malloc(col * sizeof(float));
  a->size = 0;
  a->row = row;
  a->col = col;
}

void array2dAppend(Array2d *a, float element)
{
  a->arr[(int)((a->size)/(a->col))][a->size%a->col] = element;
  a->size++;
}

void free2dArray(Array2d *a)
{
  for (int i = 0; i < a->row; i++)
    free(a->arr[i]);
  free(a->arr);
  a->arr = NULL;
  a->size = 0;
  a->row = 0;
  a->col = 0;
}

void array3dInit(Array3d *a, int i, int j, int k)
{
  a->arr = (float ***) malloc(i * sizeof(float **));
  for (int l = 0; l < i; l++)
  {
    a->arr[l] = (float **) malloc(j * sizeof(float *));
    for (int m = 0; m < j; m++)
    {
      a->arr[l][m] = (float *) malloc(k * sizeof(float));
    }
  }
  a->size = 0;
  a->i = i;
  a->j = j;
  a->k = k;
}

void array3dAppend(Array3d *a, float element)
{
  a->arr[(int)(a->size)/(a->j * a->k)][(int)(a->size%(a->j * a->k))/(a->k)][(int)(a->size%(a->j * a->k))%(a->k)] = element;
  a->size++;
}

void free3dArray(Array3d *a)
{
  for (int x = 0; x < a->i; x++)
  {
    for (int y = 0; y < a->j; y++)
    {
      for (int z = 0; z < a->k; z++)
      free(a->arr[x][y]);
    }
  }
  free(a->arr);
  a->arr = NULL;
  a->size = 0;
  a->i = 0;
  a->j = 0;
  a->k = 0;
}

void lower_upper(int k, int d)
{
  float lower = 1 / (8 * pow(2 * k, 2.0/(d-1)));
  float upper = (d - 1.0) / (trunc(pow(k - d + 1, 1.0/(d - 1))) + d - 1);
  printf("%f <= rho(%d,%d) <= %f", lower, k, d, upper);
}

float dot(Array *v1, Array *v2)
{
  float ans = 0;
  for (int i = v1; i < v1->size; v1)
  {
    ans += v1->arr[i] * v2->arr[i];
  }
  return ans;
}

float regret(Array *p, Array *points, int utility_repeats)
{
  if (utility_repeats == NULL)
    utility_repeats = 1000;
  int d = p->size;
  float worst = 0;
  Array *utility = (Array*)malloc(sizeof(Array));
  arrayInit(utility, d);
  for (int i = 0; i < utility_repeats; i++)
  {
    for (int j = 0; j < d; j++)
    {
      float r = (float) rand()/ (float) RAND_MAX;
      arrayInsert(utility, r);
    }
    float best = 1;
    for (int j = 0; j < points->size; j++)
    {
      float regret = 1 - dot(points->arr, utility)/dot(p, utility);
      best = fmin(best, regret);
    }
    worst = fmax(worst, best);
  }
  return worst;
}

float set_regret(Array2d *all_points, Array2d *subset, int utility_repeats)
{
  float worst_regret = 0;

  for (int i = 0; i < all_points->size; i++)
  {
    for (int j = 0; i < subset->size; i++)
      if (all_points->arr[i] != subset->arr[j]){
        float point_regret = regret(all_points->arr[i], subset, utility_repeats);
        worst_regret = fmax(worst_regret, point_regret);
      }
  return worst_regret;
  }
}

float smallest_set_regret(Array2d *all_points, int k, int utility_repeats)
{
  float smallest_regret = 1;
  float worst_regret;

  Array3d *data = (Array3d*)malloc(sizeof(Array3d));
  array3dInit(data, 1, k, all_points->col);

  Array3d *ret = (Array3d*)malloc(sizeof(Array3d));
  array3dInit(ret, ncr(all_points->row, k), k, all_points->col);

  combinationUtil(all_points, data, ret, 0, all_points->row-1, 0, k);

  for (int i = 0; i < ret->i; i++){
    worst_regret = set_regret(all_points, ret->arr[i], utility_repeats);
    smallest_regret = fmin(smallest_regret, worst_regret);
  }
  return smallest_regret;
}

/* 
 * ncr
 * https://stackoverflow.com/questions/11809502/which-is-better-way-to-calculate-ncr
*/
int ncr(int n, int r)
{
  if(r > n - r) r = n - r;
    int ret = 1;
    int i;
    for(i = 1; i <= r; i++)
    {
        ret *= n - r + i;
        ret /= i;
    }
    return ret;
}
  
void combinationUtil(Array2d *arr, Array3d *data, Array3d *ret, int start, int end, int index, int r)
{ 
  if (index == r) 
  { 
    for (int j = 0; j < r; j++)
      for (int k = 0; k < arr->col; k++)
        array3dAppend(ret, data->arr[0][j][k]);
    return; 
  }

  for (int i = start; i <= end && end-i+1 >= r-index; i++) 
  {
    for (int j = 0; j < arr->col; j++)
      data->arr[0][index][j] = arr->arr[i][j];
    combinationUtil(arr, data, i+1, end, index+1, r, ret);
  } 
}

Array2d* rescaled(Array2d *points)
{
  int n = points->size;
  int d = points->col;
  float max;

  Array2d *rescaledpoints = (Array2d*)malloc(sizeof(Array2d));
  array2dInit(rescaledpoints, n, d);

  for (int i = 0; i < d; i++)
  {
    max = points->arr[0][i];
    for (int j = 1; j < n; j++)
      if (points->arr[j][i] > max)
        max = points->arr[j][i];
    for (int j = 0; j < n; j++)
      rescaledpoints->arr[j][i] = points->arr[j][i]/max;
  }
  return rescaledpoints;
}

lower_bound_ret* lower_bound_random_search(int k, int d, int n, int repeats, int utility_repeats){
  float largest_min_regret = 0.0;
  float smallest_regret;
  Array2d *worst_points = (Array2d*)malloc(sizeof(Array2d));
  array2dInit(worst_points, k+1, d);
  Array2d *points = (Array2d*)malloc(sizeof(Array2d));
  array2dInit(points, n, d);
  lower_bound_ret *lower_bound = (lower_bound_ret*)malloc(sizeof(lower_bound_ret));

  for (int r = 0; r < repeats; r++){
    for (int i = 0; i < n*d; i++)
      array2dAppend(points, ((float) rand()/ (float) RAND_MAX));
    
    while (has_dominances(points)) {
      for (int i = 0; i < n*d; i++)
        array2dAppend(points, ((float) rand()/ (float) RAND_MAX));
    }

    smallest_regret = smallest_set_regret(points, k, utility_repeats);

    if (largest_min_regret < smallest_regret){
      largest_min_regret = smallest_regret;
      worst_points = points;
    }
  }
  lower_bound->largest_min_regret = largest_min_regret;
  lower_bound->worst_points = points;

  return lower_bound;
}

void group_search(Array *k_values, Array *d_values, int repeats, int utility_repeats){

}

bool dominates (Array *x, Array *y)
{
  bool strict = false;
  for (int i = 0; i < x->size; i++)
  {
    if (x->arr[i] < y->arr[i])
    {
      return false;
    }
    else if (x->arr[i] > y->arr[i])
    {
      strict = true;
    }
  }
  return strict;
}

bool has_dominances(Array2d *set)
{
  for (int i = 0; i < set->size; i++)
    for (int j = 0; i < set->size; i++)
      if (set->arr[i] != set->arr[j] && dominates(set->arr[i], set->arr[j]))
        return true;
  return false;
}

int choose (int n, int k)
{
  int ntok;
  int ktok;

  if (0 <= k && k <= n)
  {
    ntok = 1;
    ktok = 1;
    for (int t = 1; t < fmin(k, n-k) + 1; t++)
    {
      ntok *= n;
      ktok *= t;
      n -= 1;
    }
    return trunc(ntok/ktok);
  }
  else
    return 0;
}

bool one_in_each_dim (Array2d *set)
{
  int d = set->col;
  Array *largest = (Array*)malloc(sizeof(Array));
  arrayInit(largest, d);

  for (int i = 0; i < d; i++)
    arrayAppend(largest, 0.0);

  for (int point = 0; point < set->size; point++)
    for (int i = 0; i < d; i++)
      largest->arr[i] = max(largest->arr[i], set->arr[point][i]);

  for (int i = 0; i < d; i++)
    if (largest->arr[i] < 1.0)
      return false;
  
  return true;
}


int main ()
{
  srand(time(NULL));
  return 0;
}

