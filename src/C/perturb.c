#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include <time.h>

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

void arrayInit(Array *a, size_t initialSize);
void arrayAppend(Array *a, float element);
void freeArray(Array *a);
void array2dInit(Array2d *a, int row, int col);
void array2dAppend(Array2d *a, float element);
void free2dArray(Array2d *a);
void array3dInit(Array3d *a, int i, int j, int k);
void array3dAppend(Array3d *a, float element);
void freeArray3d(Array3d *a);
void freelower_bound_ret(lower_bound_ret *lower_bound);
float dot2(Array2d *v1, int x, Array *v2);
float dot3(Array3d *v1, int i, int j, Array *v2);
float regret(Array2d *p, int x, Array3d *points, int i, int utility_repeats);
float set_regret(Array2d *all_points, Array3d *subset, int i, int utility_repeats);
bool find(Array2d *all_points, int x, Array3d *subset, int i, int j);
float smallest_set_regret(Array2d *all_points, int k, int utility_repeats);
void combination(Array2d *arr, Array3d *data, Array3d *ret, int start, int end, int index, int r);
bool dominates(Array2d *set, int x, int y);
bool has_dominances(Array2d *set);
bool compare(Array2d *set, int i, int x);
int choose (int n, int k);
lower_bound_ret* lower_bound_random_search(int k, int d, int n, int repeats, int utility_repeats);

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
  a->arr[(int)((a->size)/(a->col))][a->size%a->col] = (float) element;
  a->size++;
}

void free2dArray(Array2d *a)
{
  for (int i = 0; i < a->row; i++)
    free(a->arr[i]);
  free(a->arr);
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
        free(a->arr[x][y]);
    free(a->arr[x]);
  }
  free(a->arr);
  a->size = 0;
  a->i = 0;
  a->j = 0;
  a->k = 0;
}

void freelower_bound_ret(lower_bound_ret *lower_bound){
  for (int x = 0; x < lower_bound->worst_points->row; x++)
    free(lower_bound->worst_points->arr[x]);
  free(lower_bound->worst_points->arr);
}

float dot2(Array2d *v1, int i, Array *v2)
{
  float ans = 0;
  for (int j = 0; j < v1->col; j++)
  {
    ans += v1->arr[i][j] * v2->arr[j];
  }
  return ans;
}

float dot3(Array3d *v1, int i, int j, Array *v2)
{
  float ans = 0;
  for (int k = 0; k < v1->k; k++)
  {
    ans += v1->arr[i][j][k] * v2->arr[k];
  }
  return ans;
}

float regret(Array2d *p, int x, Array3d *points, int i, int utility_repeats)
{
  int d = p->col;
  float worst = 0.0;
  //Array *utility = (Array*)malloc(sizeof(Array));
  //arrayInit(utility, d);

  for (int l = 0; l < utility_repeats; l++)
  {
    Array *utility = (Array*)malloc(sizeof(Array));
    arrayInit(utility, d);
    for (int m = 0; m < d; m++)
    {
      float r = (float)rand()/(float)RAND_MAX;
      arrayAppend(utility, r);
    }
    float best = 1.0;
    for (int j = 0; j < points->j; j++)
    {
      float regret = 1.0 - (dot3(points, i, j, utility)/dot2(p, x, utility));
      if (regret < 0)
        regret = 0.0;
      best = fmin(best, regret);
    }
    worst = fmax(worst, best);
    freeArray(utility);
    free(utility);
  }

  //freeArray(utility);
  //free(utility);
  return worst;
}

float set_regret(Array2d *all_points, Array3d *subset, int i, int utility_repeats)
{
  float worst_regret = 0;
  for (int x = 0; x < all_points->row; x++)
  {
    bool ans = false;
    for (int j = 0; j < subset->j; j++)
    {
      ans = ans || find(all_points, x, subset, i, j);
    }
    if (ans == false){
      float point_regret = regret(all_points, x, subset, i, utility_repeats);
      worst_regret = fmax(worst_regret, point_regret);
    }
  }
  return worst_regret;
}

bool find(Array2d *all_points, int x, Array3d *subset, int i, int j){
  bool ans = false;
  for (int y = 0; y < subset->k; y++)
    if (all_points->arr[x][y] == subset->arr[i][j][y])
      ans = true;
    else if (all_points->arr[x][y] != subset->arr[i][j][y])
      return false;
  return ans;
}

float smallest_set_regret(Array2d *all_points, int k, int utility_repeats)
{
  float smallest_regret = 1;
  float worst_regret;

  Array3d *data = (Array3d*)malloc(sizeof(Array3d));
  array3dInit(data, 1, k, all_points->col);

  Array3d *ret = (Array3d*)malloc(sizeof(Array3d));
  array3dInit(ret, choose(all_points->row, k), k, all_points->col);

  combination(all_points, data, ret, 0, all_points->row-1, 0, k);

  for (int i = 0; i < ret->i; i++){
    worst_regret = set_regret(all_points, ret, i, utility_repeats);
    smallest_regret = fmin(smallest_regret, worst_regret);
  }

  free3dArray(data);
  free(data);
  free3dArray(ret);
  free(ret);

  return smallest_regret;
}
  
void combination(Array2d *arr, Array3d *data, Array3d *ret, int start, int end, int index, int r)
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
    combination(arr, data, ret, i+1, end, index+1, r);
  } 
}

bool dominates (Array2d *set, int x, int y)
{
  bool strict = false;
  for (int i = 0; i < set->row; i++)
  {
    if (set->arr[x][i] < set->arr[y][i])
    {
      return false;
    }
    else if (set->arr[x][i] > set->arr[y][i])
    {
      strict = true;
    }
  }
  return strict;
}

bool has_dominances(Array2d *set)
{
  for (int i = 0; i < set->row; i++)
  {
    //for (int j = 0; j < set->col; j++)
    {
      for (int x = 0; x < set->row; x++)
      {
        //for (int y = 0; y < set->col; y++)
        if (compare(set, i, x) == true && dominates(set, i, x))
          return true;
      }
    }
  }
  return false;
}

bool compare(Array2d *set, int i, int x){
  bool ans = true;
  for (int j = 0; j < set->col; j++)
  {
    if (set->arr[i][j] != set->arr[x][j])
      return true;
    else if (set->arr[i][j] == set->arr[x][j])
      ans = false;
  }
  return ans;
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

lower_bound_ret* lower_bound_random_search(int k, int d, int n, int repeats, int utility_repeats){
  lower_bound_ret *lower_bound = (lower_bound_ret*)malloc(sizeof(lower_bound_ret));
  lower_bound->largest_min_regret = 0.0;
  lower_bound->worst_points = (Array2d*)malloc(sizeof(Array2d));
  array2dInit(lower_bound->worst_points, k+1, d);

  for (int r = 0; r < repeats; r++){
    Array2d *points = (Array2d*)malloc(sizeof(Array2d));
    array2dInit(points, n, d);
    for (int i = 0; i < n*d; i++){
      array2dAppend(points, (float)rand()/RAND_MAX);
    }
    
    while (has_dominances(points)){
      free2dArray(points);
      free(points);
      Array2d *points = (Array2d*)malloc(sizeof(Array2d));
      array2dInit(points, n, d);
      for (int i = 0; i < n*d; i++)
        array2dAppend(points, (float)rand()/RAND_MAX);
    }
    
    float smallest_regret = smallest_set_regret(points, k, utility_repeats);
    if (smallest_regret == 1.0)
      smallest_regret = 0.0;
    //printf("%f\n", smallest_regret);

    if (lower_bound->largest_min_regret < smallest_regret){
      lower_bound->largest_min_regret = smallest_regret;
      free2dArray(lower_bound->worst_points);
      array2dInit(lower_bound->worst_points, n, d);
      for (int i = 0; i < n; i++)
        for (int j = 0; j < d; j++)
        {
          printf("%f \n", points->arr[i][j]);
          lower_bound->worst_points->arr[i][j] = points->arr[i][j];
        }
    }
    free2dArray(points);
    free(points);
  }

  return lower_bound;
}

Array3d* worst_database (int k, int d, int n, int repeats, int utility_repeats){
    lower_bound_ret *lower_bound = (lower_bound_ret*)malloc(sizeof(lower_bound_ret));
    for (int i = 0; i < repeats; i++){
      lower_bound = lower_bound_random_search(k, d, n, repeats, utility_repeats);
    }

}

int main () // create default variables
{
  
  srand((unsigned)time(NULL));
  /*
  Array *k_values = (Array*)malloc(sizeof(Array));
  arrayInit(k_values, 5);
  for (int i = 2; i <= 7; i++)
    arrayAppend(k_values, i);

  Array *d_values = (Array*)malloc(sizeof(Array));
  arrayInit(d_values, 5);
  for (int i = 2; i <= 3; i++)
    arrayAppend(d_values, i);

  group_search(k_values, d_values, 1, 100);
  */

  lower_bound_ret *lower_bound = (lower_bound_ret*)malloc(sizeof(lower_bound_ret));
  lower_bound = lower_bound_random_search(2, 2, 5, 100, 100);
  printf("%f\n", lower_bound->largest_min_regret);
  for (int i = 0; i < lower_bound->worst_points->row; i++){
    for (int j = 0; j < lower_bound->worst_points->col; j++)
      printf("%f\n", lower_bound->worst_points->arr[i][j]);
    printf("\n");
  }

  printf("largest min regret: %f\n", lower_bound->largest_min_regret);
  
  freelower_bound_ret(lower_bound);
  free(lower_bound);
  
  /*
  freeArray(k_values);
  free(k_values);
  freeArray(d_values);
  free(d_values);
  */

  return 0;
}