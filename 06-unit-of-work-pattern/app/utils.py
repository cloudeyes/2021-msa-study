"""Utility functions."""

from IPython.display import SVG


# pylint: disable=too-many-locals
def show_test_pyramid(counts: dict[str, int],
                      svg_width: int = 400,
                      svg_height: int = 150,
                      margin_left: int = 150,
                      margin_right: int = 0,
                      margin_top: int = 10,
                      margin_bottom: int = 10) -> SVG:
    """테스트 피라미드를 SVG로 출력합니다.

    Args:
        counts: 테스트 항목(`e2e`, `integration`, `unit`)별 키에 대한 갯수입니다.
    """

    e2e, intg, unit = [
        counts.get(it, 0) for it in ('e2e', 'integration', 'unit')
    ]
    max_cnt = max(counts.values())

    width = svg_width - margin_left - margin_right
    height = svg_height - margin_top - margin_bottom

    unit_width = width // max_cnt
    unit_height = height // 2

    bottom_left = margin_left + (
        width - unit_width * unit) // 2, unit_height * 2 + margin_top
    bottom_right = bottom_left[
        0] + unit_width * unit, unit_height * 2 + margin_top

    mid_left = margin_left + (
        width - unit_width * intg) // 2, unit_height * 1 + margin_top
    mid_right = mid_left[0] + unit_width * intg, unit_height * 1 + margin_top

    top_left = margin_left + (
        width - unit_width * e2e) // 2, unit_height * 0 + margin_top
    top_right = top_left[0] + unit_width * e2e, unit_height * 0 + margin_top

    points = f'{bottom_left} {mid_left} {top_left} {top_right} {mid_right} {bottom_right}'
    points = points.replace('(', '').replace(')', '').replace(', ', ',')

    svg_output = f'''
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}"
      width="{svg_width}" height="{svg_height}">
      <polygon points="{points}"
       style="fill:none;stroke:black;stroke-width:2"/>
       <text x="{0}" y="{bottom_left[1]-5}">unit: {unit}</text>
       <text x="{0}" y="{mid_left[1]+margin_top-10}">integration: {intg}</text>
       <text x="{0}" y="{top_left[1]+margin_top}">e2e: {e2e}</text>
    </svg>
    '''

    return SVG(svg_output)
