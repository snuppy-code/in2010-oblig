from test_output import main
main(
    shortest_queries = [['nm1', 'nm2'], ['nm1', 'nm3']],
    chillest_queries = [['nm1', 'nm2'], ['nm1', 'nm3']],
    component_sizes = {(1, 1), (1, 3)},
    movies = {'tt2': ('Movie B', 9.0, ['nm1', 'nm3']), 'tt3': ('Movie C', 9.0, ['nm2', 'nm3']), 'tt1': ('Movie A', 5.0, ['nm1', 'nm2'])},
    actors = {'nm3': ('Carol', ['tt2', 'tt3']), 'nm2': ('Bob', ['tt1', 'tt3']), 'nm1': ('Alice', ['tt1', 'tt2'])},
    shortest_query_answers = [1, 1],
    chillest_query_answers = [2.0, 1.0],
)
