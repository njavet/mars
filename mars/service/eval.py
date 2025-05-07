class Evaluator:
    def __init__(self):



def run_eval(base_url, system_message, result_dir):
    lms = get_lms(base_url)
    print(system_message)
    for docx_path in DOCX_DIR.glob('*.docx'):
        start_t = time.time()
        text = read_docx(docx_path)
        print('evaluating {}'.format(docx_path))
        results = EvaluationResult(server=base_url,
                                   filename=docx_path.name,
                                   system_message=system_message)
        for lm_name in lms:
            print('lm_name: ', lm_name)
            res_chat = run_baseline(base_url=base_url,
                                    lm_name=lm_name,
                                    system_message=system_message,
                                    query=text)
            results.lm_names.append(lm_name)
            results.outputs.append(format_as_markdown(res_chat))
        output_path = Path.joinpath(result_dir, docx_path.stem + '.json')
        with open(output_path, 'w') as f:
            json.dump(results.model_dump(), f, indent=2,
                      ensure_ascii=False)

        print(
            'evaluation took {:.2f} seconds'.format(time.time() - start_t))

